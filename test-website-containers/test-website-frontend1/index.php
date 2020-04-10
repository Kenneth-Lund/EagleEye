<html>
    <head>
        <title>Northrop Grumman Site 1</title>
    </head>

    <body>
        <h1>If you are on this site, you have reached the first secret website.</h1>
        <h2> Click <a href="http://127.0.0.1:5002/">here</a> to go to the second secret website.</h2>
        <h2> Click <a href="http://127.0.0.1:5003/">here</a> to go to the third secret website.</h2>
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
