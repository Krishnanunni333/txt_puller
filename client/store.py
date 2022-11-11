import click
import upload

@click.group()
def cli():
    pass

@cli.command("add")
@click.argument('files', type=str, nargs=-1)
def add(files):
    upload.push(files)

@cli.command("ls")
def ls():
    click.echo("ls")

@cli.command("rm")
def rm():
    click.echo("rm")

@cli.command("update")
def update():
    click.echo("update")

@cli.command("wc")
def wc():
    click.echo("wc")

@cli.command("freq-words")
def freq_words():
    click.echo("freq-words")


if __name__ == '__main__':
    cli()