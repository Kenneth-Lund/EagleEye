<html>
    <head>
        <title>Northrop Grumman Site 2</title>
    </head>

    <body>
        <!-- Hello there, this is a test. (324)-324-2324 -->
        <img src="./pictures/logo.png" style="width:350px;height:150px;">
        <h1>Test Website 2</h1>
        <h2>If you are on this site, you have reached the second test website.</h2>
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
