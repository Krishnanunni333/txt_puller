import click
import controller
import logging

@click.group()
def cli():
    pass

@cli.command("add")
@click.argument('files', type=str, nargs=-1)
def add(files):
    try:
        controller.push(files)
    except Exception as e:
        logging.error(e, exc_info=True)

@cli.command("ls")
def ls():
    try:
        click.secho(*controller.listfiles(), fg="green", bold=True)
    except Exception as e:
        logging.error(e, exc_info=True)
    

@cli.command("rm")
@click.argument('filename', type=str)
def rm(filename):
    try:
        controller.remove_file(filename)
    except Exception as e:
        logging.error(e, exc_info=True)

@cli.command("update")
def update():
    click.echo("update")

@cli.command("wc")
def wc():
    controller.count_total_words()

@cli.command("freq-words")
def freq_words():
    click.echo("freq-words")


if __name__ == '__main__':
    cli()