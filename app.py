from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Item
import os

def create_app(db_path="sqlite:///database.db"):
    app = Flask(__name__)
    # 用于 flash 消息
    app.secret_key = os.environ.get("REVIVE_SECRET", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # --- Web Routes ---
    @app.route("/", methods=["GET"])
    def index():
        """
        首页：显示物品列表并支持 ?q= 查询参数（模糊搜索 name/description/contact）
        """
        q = request.args.get("q", "").strip()
        if q:
            # 模糊匹配 name/description/contact（不区分大小写）
            like = f"%{q}%"
            items = Item.query.filter(
                db.or_(
                    Item.name.ilike(like),
                    Item.description.ilike(like),
                    Item.contact.ilike(like)
                )
            ).order_by(Item.created_at.desc()).all()
            flash(f"搜索结果：{len(items)} 项，关键字：{q}", "info")
        else:
            items = Item.query.order_by(Item.created_at.desc()).all()
        return render_template("index.html", items=items, q=q)

    @app.route("/add", methods=["GET", "POST"])
    def add_item():
        """添加物品页面与处理"""
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            contact = request.form.get("contact", "").strip()
            if not name:
                flash("物品名称为必填项。", "danger")
                return redirect(url_for("add_item"))
            item = Item(name=name, description=description or None, contact=contact or None)
            db.session.add(item)
            db.session.commit()
            flash("物品已添加。", "success")
            return redirect(url_for("index"))
        return render_template("add.html")

    @app.route("/view/<int:item_id>", methods=["GET"])
    def view_item(item_id):
        """查看物品详情"""
        item = Item.query.get_or_404(item_id)
        return render_template("view.html", item=item)

    @app.route("/delete/<int:item_id>", methods=["POST"])
    def delete_item(item_id):
        """删除物品（POST）"""
        item = Item.query.get(item_id)
        if not item:
            flash("未找到该物品。", "warning")
            return redirect(url_for("index"))
        db.session.delete(item)
        db.session.commit()
        flash("物品已删除。", "success")
        return redirect(url_for("index"))

    # --- 简单 JSON API ---
    @app.route("/api/items", methods=["GET", "POST"])
    def api_items():
        if request.method == "GET":
            q = request.args.get("q", "").strip()
            if q:
                like = f"%{q}%"
                items = Item.query.filter(
                    db.or_(
                        Item.name.ilike(like),
                        Item.description.ilike(like),
                        Item.contact.ilike(like)
                    )
                ).order_by(Item.created_at.desc()).all()
            else:
                items = Item.query.order_by(Item.created_at.desc()).all()
            return jsonify([it.to_dict() for it in items]), 200
        else:
            data = request.json or {}
            name = (data.get("name") or "").strip()
            if not name:
                return jsonify({"error": "name required"}), 400
            item = Item(name=name, description=data.get("description"), contact=data.get("contact"))
            db.session.add(item)
            db.session.commit()
            return jsonify(item.to_dict()), 201

    @app.route("/api/items/<int:item_id>", methods=["GET", "DELETE"])
    def api_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "not found"}), 404
        if request.method == "GET":
            return jsonify(item.to_dict()), 200
        else:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"ok": True}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    # 调试模式可选（开发时打开）
    app.run(host="0.0.0.0", port=5000, debug=True)
