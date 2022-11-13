from click.testing import CliRunner
import create_test_txt
from store import ls, add, wc, freq_words, rm, update
import glob

runner = CliRunner()
create_test_txt.create_test_files()


def test_add():
    test_txt_files = [i[2:] for i in glob.glob('./*.txt')]
    response = runner.invoke(add, test_txt_files)
    assert response.exit_code == 0
    assert 'SUCCESS' in response.output

def test_ls():
    response = runner.invoke(ls)
    assert response.exit_code == 0
    assert  "ALL FILES" in response.output

def test_rm():
    test_txt_files = [i[2:] for i in glob.glob('./*.txt')]
    response = runner.invoke(rm, test_txt_files[0])
    assert response.exit_code == 0
    assert  "SUCCESS" in response.output and test_txt_files[0] in response.output
    create_test_txt.remove_file_in_local(test_txt_files[0])

def test_wc():
    test_txt_files = [i[2:] for i in glob.glob('./*.txt')]
    word_count = create_test_txt.word_count(test_txt_files)
    response = runner.invoke(wc)
    assert response.exit_code == 0
    assert  "SUCCESS" in response.output and str(word_count) in response.output

def test_update():
    pass

def test_freq_words():
    freq_count_local = create_test_txt.get_freq_words()
    response =  runner.invoke(freq_words, ["-n", 10, "--order", "asc"])
    assert response.exit_code == 0
    assert  "SUCCESS" in response.output and any([True for i in freq_count_local if i not in response.output])

