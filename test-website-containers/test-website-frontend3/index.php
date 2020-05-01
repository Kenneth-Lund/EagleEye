<html>
    <head>
        <title>Northrop Grumman Site 3</title>
    </head>

    <body>
        <!-- Hello there, this is a test. (234) 33-7853 -->
        <img src="./pictures/logo.png" style="width:350px;height:150px;">
        <h1>Test Website 3</h1>
        <h2>If you are on this site, you have reached the third test website.</h1>
        <h2> Click <a href="http://127.0.0.1:5000/">here</a> to go back to the first secret website.</h2>
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
