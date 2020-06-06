<h1>python-project-lvl3</h1>
<div>
  <p>
    <a href="https://codeclimate.com/github/sdemikhov/python-project-lvl3/maintainability"><img src="https://api.codeclimate.com/v1/badges/6e5bd221dd513f646112/maintainability" /></a>
    <a href="https://travis-ci.org/sdemikhov/python-project-lvl3"><img src="https://travis-ci.org/sdemikhov/python-project-lvl3.svg?branch=master" /></a>
  </p>
  <p>Page-loader is a CLI tool to download web pages.</p>
  <h2>Install Page-loader:</h2>
  <pre>pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/pypi/ sdemikhov-page-loader</pre>
  <ul>
    <li>use <em>pip install --user</em> to install packages into your day-to-day default Python environment.</li>
   </ul>
  <h2>Run Page-loader:</h2>
<pre>
usage: page-loader [-h] [-o OUTPUT] [-l LOG_LEVEL] target_url

Page-loader

positional arguments:
  target_url            URL to target page

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Set directory for saved page
  -l LOG_LEVEL, --log LOG_LEVEL
                        Set level of logging information: 'none', 'warning',
                        'debug'
</pre>
  <h2>Development process:</h2>
  <ul>
    <li>
      <p>Download web page to choosen directory and cwd:</p>
      <p><a href="https://asciinema.org/a/hPtCshE94U1CyxID48RGDE2qg" target="_blank"><img src="https://asciinema.org/a/hPtCshE94U1CyxID48RGDE2qg.svg" /></a></p>
    </li>
      <li>
      <p>Download web page and local resources:</p>
      <p><a href="https://asciinema.org/a/Qzq2CBnzMGm41gxNffuXe0MX9" target="_blank"><img src="https://asciinema.org/a/Qzq2CBnzMGm41gxNffuXe0MX9.svg" /></a></p>
    </li>
      <li>
      <p>Added logger to project:</p>
      <p><a href="https://asciinema.org/a/Sgftcnm4ac1Axn5YPeggPogk5" target="_blank"><img src="https://asciinema.org/a/Sgftcnm4ac1Axn5YPeggPogk5.svg" /></a></p>
    </li>
    <li>
      <p>Exception handling:</p>
      <p><a href="https://asciinema.org/a/gvcuLP2wdhLG28ZT5ktIZsvC0" target="_blank"><img src="https://asciinema.org/a/gvcuLP2wdhLG28ZT5ktIZsvC0.svg" /></a></p>
    </li>
    <li>
      <p>Progress bar:</p>
      <p><a href="https://asciinema.org/a/SC5k5bLjW9Je0Fx93tx8YLaNb" target="_blank"><img src="https://asciinema.org/a/SC5k5bLjW9Je0Fx93tx8YLaNb.svg" /></a></p>
    </li>
  </ul>
</div>
