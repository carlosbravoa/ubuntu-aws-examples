<html>
<head>
    <title>PHP Container Test page</title>
    <style type="text/css" media="screen">
        .hl{ background: #D3E18A;}
        h2 {margin-bottom: 0px;}
        .ex { font-size: .7em;
            font-style: italic;
            margin-bottom: 2em;
            }
        body {
        font-family: "Ubuntu", "Segoe UI", "Roboto", "Oxygen", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
        margin: 0;
        }

        h2 {
            display: block;
            font-size: 1.5em;
            margin-block-start: 0.83em;
            #margin-block-end: 0.83em;
            margin-inline-start: 0px;
            margin-inline-end: 0px;
            font-weight: bold;
        }

        h1 {
            display: block;
            font-size: 2em;
            margin-block-start: 0.67em;
            margin-block-end: 0.67em;
            margin-inline-start: 0px;
            margin-inline-end: 0px;
            font-weight: bold;
        }

        pre {
            background: none;
            box-shadow: none;
            display: inline-block;
            line-height: 1.5rem;
            margin-left: 0;
            margin-right: 0;
            padding: 0;
            background-color: rgba(0,0,0,.03);
            color: #111;
            display: block;
            margin-bottom: 1.5rem;
            margin-top: 0;
            overflow: auto;
            padding: 0.5rem 1rem;
            text-align: left;
            text-shadow: none;
            white-space: pre;
        }

        .banner {
                background-color: #772953;
                background-image: linear-gradient(-89deg, #e95420 0%, #772953 42%, #2c001e 94%);
                color: #fff;
                padding: 2em;
        }
        #results {
                margin-left: 2em;
        }

    </style>
</head>
<body>

<div class="banner">
<h1>PHP-container basic test</h1>
<p>If you are seeing this page, that means that everything worked!</p>
</div>

<div id="results">

<h2>Additional information</h2>
<h3>Kernel information (host)</h2>
<?php
$output = shell_exec('uname -a');
echo "<pre>Uname: $output</pre>";
?>

<h3>Release used in container</h2>
<?php
$output = shell_exec('cat /etc/os-release');
echo "<pre>Uname: $output</pre>";
?>

<h3>Packages in container with ESM updates (i.e. security fixes from Canonical):</h2>
<?php
$output = shell_exec('dpkg -l | grep esm');
echo "<pre>$output</pre>";
?>

</div>

</body>
</html>


