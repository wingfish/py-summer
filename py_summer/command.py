import os
import sys
import click
import shutil
import json
from py_summer import app, db

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))


@click.group()
def cli():
    """
    summer server 启动命令行管理工具
    """


@click.command()
def create_tables():
    """
    删除当前数据库内容，并创建数据库
    """
    click.echo(click.style('Create db tables.', fg='red'))
    db.drop_all()
    db.create_all()
    click.echo(click.style('Tables created success.', fg='blue'))


@click.command('start')
@click.option('--reload', default=False, type=click.BOOL, help='是否自动重新加载服务')
def start_server(reload):
    """
    启动 server
    """
    click.echo(click.style('server start', fg='blue'))
    app.run(use_reloader=reload, host='127.0.0.1', port=app.config['IP_PORT'])


@click.command('create_project')
@click.option('--name', default='py_summer_demo', type=click.STRING, help='项目名称', prompt='项目名称',
              required=True)
@click.option('--path', default='./', type=click.STRING, help='项目路径', prompt='项目路径', required=True)
def create_project(name, path):
    """
    创建新项目
    :param name: 项目路径
    :param path: 项目名称
    :return:
    """
    project_full_path = os.path.join(path, name)
    if os.path.exists(project_full_path):
        shutil.rmtree(project_full_path)
    os.makedirs(project_full_path)
    with open('./tpl/config.json', "r") as f:
        config = json.load(f)
    structure = config.get('structure')
    _create_file_folder(structure, project_full_path)


def _create_file_folder(structure, project_full_path):
    """
    根据配置文件夹创建文件和文件夹
    :param structure: 配置文件
    :param project_full_path: 项目路径
    :return:
    """
    for item in structure:
        name = item.get('name')
        is_folder = item.get('is_folder')
        child = item.get('child')
        current_path = os.path.join(project_full_path, name)

        if is_folder:
            _create_folder(current_path)
            _create_file_folder(child, current_path)
        else:
            tpl = item.get('content')
            _create_file(current_path, tpl)


def _create_folder(folder_path):
    """
    创建文件夹
    :param folder_path:
    :return:
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    else:
        os.makedirs(folder_path)


def _create_file(file_path, tpl_name):
    """
    生成文件，根据模版
    :param file_path:
    :param tpl_name:
    :return:
    """
    tpl_file_path = os.path.join('.', 'tpl', tpl_name)
    _buffer = open(tpl_file_path, 'rb')
    with open(file_path, 'wb') as f:
        f.write(_buffer.read())
    _buffer.close()


# server 主要执行过程
if __name__ == '__main__':
    cli.add_command(start_server)
    cli.add_command(create_tables)
    cli.add_command(create_project)
    cli()