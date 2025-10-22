import sys
import click
from app import create_app
from models import db, Item

app = create_app()
ctx = app.app_context()
ctx.push()

@click.group()
def cli():
    pass

@cli.command()
@click.option("--name", prompt="物品名称", help="要添加的物品名称")
@click.option("--description", prompt="物品描述", default="", help="物品描述")
@click.option("--contact", prompt="联系人/联系方式", default="", help="联系人信息")
def add(name, description, contact):
    """添加物品"""
    item = Item(name=name.strip(), description=(description.strip() or None), contact=(contact.strip() or None))
    db.session.add(item)
    db.session.commit()
    click.echo(f"已添加物品 id={item.id} name={item.name}")

@cli.command("list")
def _list():
    """列出所有物品（按时间倒序）"""
    items = Item.query.order_by(Item.created_at.desc()).all()
    if not items:
        click.echo("当前没有物品。")
        return
    for it in items:
        click.echo(f"[{it.id}] {it.name} | contact: {it.contact or '-'} | created: {it.created_at} \n    {it.description or ''}")

@cli.command()
@click.argument("term", required=True)
def search(term):
    """按名称/描述/联系人模糊搜索"""
    like = f"%{term}%"
    items = Item.query.filter(
        db.or_(
            Item.name.ilike(like),
            Item.description.ilike(like),
            Item.contact.ilike(like)
        )
    ).order_by(Item.created_at.desc()).all()
    if not items:
        click.echo("未找到匹配项。")
        return
    for it in items:
        click.echo(f"[{it.id}] {it.name} | contact: {it.contact or '-'} | created: {it.created_at} \n    {it.description or ''}")

@cli.command()
@click.argument("item_id", type=int)
def delete(item_id):
    """删除指定 id 的物品"""
    it = Item.query.get(item_id)
    if not it:
        click.echo("未找到该物品。")
        return
    confirm = click.confirm(f"确定删除 [{it.id}] {it.name} 吗？")
    if not confirm:
        click.echo("已取消。")
        return
    db.session.delete(it)
    db.session.commit()
    click.echo("已删除。")

if __name__ == "__main__":
    cli()
