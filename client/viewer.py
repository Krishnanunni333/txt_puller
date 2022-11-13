import click


def display_error(content):
    click.secho("ERROR: \n{}".format(content), fg="red", bold=True)

def display_success(content):
    click.secho("----SUCCESS---- \n{}".format(content), fg="green", bold=True)

def display_warning(content):
    click.secho("WARNING: \n{}".format(content), fg="yellow", bold=True)

def display_files(content):
    click.secho("----------ALL FILES---------\n{}".format(content), fg="blue", bold=True)