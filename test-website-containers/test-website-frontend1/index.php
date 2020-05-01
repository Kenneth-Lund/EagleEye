<html>
    <head>
        <title>Northrop Grumman Site 1</title>
        <script>
            /*       
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
            */
        </script>
    </head>
    <body>
        <img src="./pictures/logo.png" style="width:350px;height:150px;">
        <h1>Test Website 1</h1>
        <h2> Click <a href="http://127.0.0.1:5002/">here</a> to go to the second test website.</h2>
        <h2> Click <a href="http://127.0.0.1:5003/">here</a> to go to the third test website.</h2>
        <!-- Hello there, this is a test. commentEmail@gmail.com -->
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
        <h2>This user: user.name+tag+sorting@example.com contacted this email: tester04@gmail.com</h2>
        <h2>Employee 5 with SSN: 111-11-0012 is relatives with the person having SSN: 213-25-4000</h2>
        <br></br>
        <h2>Reach Employee 0321 at 230-345-2145</h2>
        <h2>Reach Employee 3245 at (543)-123-9942</h2>
    </body>
</html>
