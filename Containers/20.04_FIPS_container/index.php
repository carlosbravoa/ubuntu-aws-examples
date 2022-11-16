<html>
<head>
    <title>FIPS Test page</title>
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
<h1>FIPS basic test</h1>
<p>This page shows different ways to see whether FIPS mode is enabled and working. These tests are only for demonstration and it should not be used or hosted on production environments. All the tests shown here are intended to be run directly on the console and not from a webpage</p>
</div>

<div id="results">
<?php

$is_FIPS_enabled = shell_exec('cat /proc/sys/crypto/fips_enabled');


if ($is_FIPS_enabled) {
        echo "<h2>Congratulations, your system is running on FIPS mode</h2>";
}
else {
        echo "<h2>Your system is NOT running on FIPS mode</h2>";
}


echo '<h2>Host (worker nodes) information</h2>';


#$output = shell_exec('lsb_release -d -s');
#echo "<div>OS and release version: $output </div>";

$output = shell_exec('uname -a');
echo "<div class='ex'>It should contain the word fips in the kernel name if you are on a FIPS kernel</div>";
echo "<pre>Uname: $output</pre>";

echo '<h2>Ubuntu Advantage status:</h2>';
echo "<div class='ex'>Containers normally don't include UA/Pro subscriptions, so it is normal if this is empty</div>";
$output = shell_exec('ua status');
echo "<pre>$output</pre>";

echo '<h2>Is FIPS enabled (file check):</h2>';
echo "<div class='ex'>You should see a '1' next to the following text. If not, Sthe file does not exist, therefore Kernel is not running on FIPS mode</div>";

echo "<pre>fips_enabled file exists: $is_FIPS_enabled</pre>";

echo '<h2>Packages in container with FIPS:</h2>';
$output = shell_exec('dpkg -l | grep fips');
echo "<pre>$output</pre>";
?>

</div>

<script>
let textElement = document.getElementById("results");
let text = textElement.innerHTML;
text = text.replace(/fips/g, "<span class='hl'>FIPS</span>");
textElement.innerHTML = text;

</script>
</body>
</html>
