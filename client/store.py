import click
import controller
import logging
import viewer as view

@click.group()
def cli():
    pass

@cli.command("add")
@click.argument('files', type=str, nargs=-1)
def add(files):
    try:
        content, error = controller.push(files)
        if error != None:
            view.display_error(error)
        else:
            view.display_success(content)
    except Exception as e:
        logging.error(e, exc_info=True)

@cli.command("ls")
def ls():
    try:
        content, error = controller.listfiles()
        if error != None:
            view.display_error(error)
        else:
            view.display_files("\n".join(content))
    except Exception as e:
        logging.error(e, exc_info=True)
    

@cli.command("rm")
@click.argument('filename', type=str)
def rm(filename):
    try:
        content, error = controller.remove_file(filename)
        if error != None:
            view.display_error(error)
        else:
            view.display_success(content)
    except Exception as e:
        logging.error(e, exc_info=True)

@cli.command("update")
@click.argument('filename', type=str)
def update(filename):
    try:
        content, error = controller.update_file(filename)
        if error != None:
            view.display_error(error)
        else:
            view.display_files("\n".join(content))
    except Exception as e:
        logging.error(e)

@cli.command("wc")
def wc():
    try:
        content, error = controller.count_total_words()
        if error != None:
            view.display_error(error)
        else:
            view.display_success(content)
    except Exception as e:
        logging.error(e)

@cli.command("freq-words")
@click.option('-n', '--limit', required=True, type=int, help="Provide the limit")
@click.option('--order', required=True, type=str, help="Provide the sorting oder, asc for least frequent and asc for most frequent")
def freq_words(limit, order):
    try:
        content, error = controller.freq_words(limit, order)
        if error != None:
            view.display_error(error)
        else:
            view.display_success("\n".join(content))
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    cli()