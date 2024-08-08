document.addEventListener('DOMContentLoaded', function() {
    let userId;

    fetchCurrentUserId();

    function fetchCurrentUserId() {
        fetch("/api/current_user")
            .then(response => response.json())
            .then(data => {
                if (data.user_id) {
                    userId = data.user_id;
                    console.log("User ID set:", userId);
                } else {
                    console.error("User not logged in");
                }
            })
            .catch(error => {
                console.error("Error fetching user ID:", error);
            });
    }

    function startScanner() {
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#scanner-container'),
                constraints: {
                    width: 480,
                    height: 320,
                    facingMode: "environment"
                },
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "ean_8_reader", "upc_reader"]
            }
        }, function(err) {
            if (err) {
                console.error(err);
                return;
            }
            console.log("Quagga initialization finished. Ready to start");
            Quagga.start();
        });

        Quagga.onDetected(function(result) {
            const code = result.codeResult.code;
            document.getElementById('barcode').value = code;
            Quagga.stop();
        });
    }

    document.getElementById('scanForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const barcode = document.getElementById('barcode').value;
        const price = parseFloat(document.getElementById('price').value);
        const saleStatus = document.getElementById('sale_status').checked;
        const tags = document.getElementById('tags').value.split(',').map(tag => tag.trim());

        const scanData = {
            barcode: barcode,
            price: price,
            sale_status: saleStatus,
            tags: tags,
            user_id: userId
        };

        fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(scanData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById('scanResult').innerHTML = `<p>${data.message}</p>`;
            } else {
                document.getElementById('scanResult').innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch(error => console.error('Error scanning item:', error));
    });

    startScanner();
});
