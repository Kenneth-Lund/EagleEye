<html>
    <head>
        <title>Northrop Grumman</title>
    </head>

    <body>
        <h1>If you are on this site, you have reach secret stuff.</h1>
        <ul>
            <?php

            $json = file_get_contents('http://test-website-backend/get-data');
            $obj = json_decode($json);

            $sensitive_data = $obj->sensitive_data;

            foreach ($sensitive_data as $data_key) {
                echo "<li>$data_key</li>";
            }

            ?>
        </ul>
    </body>
</html>
