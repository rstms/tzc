from click.testing import CliRunner
from tzc.main import cli
from pathlib import Path


def test_conversion(shared_datadir):
    INPUT_LINE = '2021-01-01 01:01:02.345678+00:00 test2'
    OUTPUT_LINE = '2020-12-31 19:01:02.345678-06:00 test2'
    _test(shared_datadir, INPUT_LINE, OUTPUT_LINE, ['-o', 'US/Central'])

def test_short_format(shared_datadir):
    INPUT_LINE = '2021-01-01 01:01:02.345678+00:00 test2'
    OUTPUT_LINE = '2020-12-31 19:01:02 test2'
    _test(shared_datadir, INPUT_LINE, OUTPUT_LINE, ['--short', '--output-zone', 'US/Central'])

def test_custom_format(shared_datadir):
    INPUT_LINE = '2021-01-01 01:01:02.345678+00:00 test2'
    OUTPUT_LINE = '20201231190102 test2'
    _test(shared_datadir, INPUT_LINE, OUTPUT_LINE, ['-f', '%Y%m%d%H%M%S', '-o', 'US/Central'])

def test_custom_format_and_short_timezone(shared_datadir):
    INPUT_LINE = '2021-01-01 01:01:02.345678+00:00 test2'
    OUTPUT_LINE = '20201231200102 test2'
    _test(shared_datadir, INPUT_LINE, OUTPUT_LINE, ['-f', '%Y%m%d%H%M%S', '-o', 'EST'])

def _test(shared_datadir, input_line, output_line, clargs):
    ifile = Path(shared_datadir) / 'infile'
    ofile = Path(shared_datadir) / 'outfile'
    with ifile.open('w') as fp:
        fp.write('test1\n')
        fp.write(input_line + '\n')
        fp.write('test3\n')
    clargs.insert(0, str(ofile))
    clargs.insert(0, str(ifile))
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, clargs)
    assert result.exit_code == 0
    assert ofile.is_file()
    with ofile.open('r') as fp:
        lines = [line.strip() for line in fp]
    assert len(lines)==3
    assert lines[0]=='test1'
    assert lines[1]==output_line
    assert lines[2]=='test3'

def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")

def test_file(shared_datadir):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(Path(shared_datadir)/'log'), '-o', 'US/Central', '-s'])
        assert result.exit_code == 0
        lines = result.output.split('\n')
        assert len(lines)==11
        for line in lines:
            if line.startswith('2021'):
                assert line.startswith('2021-01-25 14')
    
