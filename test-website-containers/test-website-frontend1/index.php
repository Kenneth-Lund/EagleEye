<html>
    <head>
        <title>Northrop Grumman Site 1</title>

        <script>

            var i = 0;

            // update site content every second
            setInterval(function() {

                // get div with id example
                var myElement = document.getElementById('test_count');

                // count up by 1
                i++;

                // update content
                myElement.innerHTML = 'Time visited: ' + i;

            }, 1000);
        </script>
    </head>
    <body>
        <h1>If you are on this site, you have reached the first secret website.</h1>
        <h2> Click <a href="http://127.0.0.1:5002/">here</a> to go to the second secret website.</h2>
        <h2> Click <a href="http://127.0.0.1:5003/">here</a> to go to the third secret website.</h2>
        <ul>
            <?php

            $count = 0;

            $json = file_get_contents('http://test-website-backend/get-data');
            $obj = json_decode($json);

            $sensitive_data = $obj->sensitive_data;

            foreach ($sensitive_data as $data_key) {
                echo "<li>$data_key</li>";
            }

            ?>
        </ul>
        <h2 id = "test_count"> Time visited: 0 </h2>
    </body>
</html>
