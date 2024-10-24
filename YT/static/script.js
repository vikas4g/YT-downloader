document.getElementById('downloadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var url = document.getElementById('url').value;
    var format = document.getElementById('format').value;

    // Start the download request via AJAX
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'url': url,
            'format': format
        })
    }).then(response => response.json())
      .then(data => {
          if (data.message === "Download started") {
              document.getElementById('progressContainer').style.display = 'block';
              pollProgress();  // Start polling for progress updates
          } else {
              alert(data.message);
          }
      });
});

function pollProgress() {
    var interval = setInterval(function () {
        fetch('/progress')
            .then(response => response.json())
            .then(data => {
                var progressBarFill = document.getElementById('progressBarFill');
                var progressText = document.getElementById('progressText');

                if (data.status === 'downloading') {
                    progressBarFill.style.width = data.percentage + '%';
                    progressText.innerText = data.percentage.toFixed(2) + '%';
                } else if (data.status === 'finished') {
                    progressBarFill.style.width = '100%';
                    progressText.innerText = 'Download Complete!';
                    clearInterval(interval);  // Stop polling once the download is complete
                }
            });
    }, 2000);  // Poll every 2 seconds
}
