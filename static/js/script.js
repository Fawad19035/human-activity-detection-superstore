// script.js
$(document).ready(function() {
    let videoFile = null; // Stores the uploaded video file
    let activityUpdateInterval; // Interval for polling activity updates
    let currentSource = null; // Tracks current video source (webcam/rtsp)

    // Initialize Bootstrap tabs (if needed dynamically)
    const tabEl = document.querySelector('#sourceTab');
    const tab = new bootstrap.Tab(tabEl);

    // Function to start the video feed
    function startVideoFeed(sourceType, source = null) {
        stopVideoFeed(); // Stop any running feed first

        $.ajax({
            url: '/start_feed',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ source_type: sourceType, source: source }),
            success: function(data) {
                if (data.error) {
                    showError('rtsp-status', data.error);
                } else {
                    currentSource = sourceType;
                    $('#video-feed').attr('src', '/video_feed'); // Show live feed image
                    if (sourceType === 'rtsp') {
                        showSuccess('rtsp-status', `Connected to CCTV at ${source}`);
                    }
                    activityUpdateInterval = setInterval(updateActivityStats, 1000); // Poll every second
                }
            },
            error: function(xhr) {
                const errorMsg = xhr.responseJSON?.error || 'Failed to start video feed';
                showError('rtsp-status', errorMsg);
            }
        });
    }

    // Stop the video feed
    function stopVideoFeed() {
        $.get('/stop_feed', function(data) {
            $('#video-feed').attr('src', '');
            clearInterval(activityUpdateInterval);
            currentSource = null;
        });
    }

    // Get activity statistics (polling from server)
    function updateActivityStats() {
        $.get('/get_activity_count', function(data) {
            $('#activity-count').text(data.count);
            $('#feed-timestamp').text(new Date(data.timestamp).toLocaleTimeString());
            if (data.activities && data.activities.length > 0) {
                $('#recent-activities').html("Recent: " + data.activities.join(", "));
            } else {
                $('#recent-activities').html("Recent: None");
            }
        });
    }

    // Show a green success message
    function showSuccess(elementId, message) {
        $(`#${elementId}`)
            .removeClass()
            .addClass('status success')
            .html(`<i class="fas fa-check-circle me-2"></i> ${message}`)
            .show();
    }

    // Show a red error message
    function showError(elementId, message) {
        $(`#${elementId}`)
            .removeClass()
            .addClass('status error')
            .html(`<i class="fas fa-exclamation-triangle me-2"></i> ${message}`)
            .show();
    }

    // Setup all event listeners for buttons and inputs
    function setupEventListeners() {
        // Start and stop webcam
        $("#start-webcam").click(function() {
            startVideoFeed('webcam');
        });

        $("#stop-webcam").click(function() {
            stopVideoFeed();
        });

        // Test RTSP stream connection
        $("#test-rtsp").click(function() {
            const rtspUrl = $("#rtsp-url").val();
            if (!rtspUrl) {
                showError('rtsp-status', 'Please enter RTSP URL');
                return;
            }

            $('#rtsp-status')
                .removeClass()
                .addClass('status processing')
                .html('<i class="fas fa-spinner fa-spin me-2"></i> Testing connection...')
                .show();

            $.ajax({
                url: '/test_rtsp',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ rtsp_url: rtspUrl }),
                success: function(data) {
                    if (data.error) {
                        showError('rtsp-status', data.error);
                    } else {
                        showSuccess('rtsp-status', data.message);
                    }
                },
                error: function(xhr) {
                    const errorMsg = xhr.responseJSON?.error || 'Connection test failed';
                    showError('rtsp-status', errorMsg);
                }
            });
        });

        // Start RTSP stream
        $("#start-rtsp").click(function() {
            const rtspUrl = $("#rtsp-url").val();
            if (!rtspUrl) {
                showError('rtsp-status', 'Please enter RTSP URL');
                return;
            }
            startVideoFeed('rtsp', rtspUrl);
        });

        // Video upload handler
        $("#video-upload").change(function(e) {
            if (e.target.files.length > 0) {
                videoFile = e.target.files[0];

                // Check if file size is within 100MB
                if (videoFile.size > 100 * 1024 * 1024) {
                    showError('upload-status', 'File size exceeds 100MB limit');
                    $("#process-btn").prop("disabled", true);
                    return;
                }

                showSuccess('upload-status', `${videoFile.name} uploaded successfully!`);
                $("#process-btn").prop("disabled", false);
                $("#results-section").hide();
                $("#video-container").hide();
            }
        });

        // Analyze uploaded video
        $("#process-btn").click(function() {
            if (!videoFile) return;

            // Reset video UI
            $("#video-player").attr("src", "");
            $("#video-container").hide();
            $("#play-overlay").hide();

            $("#processing-status")
                .removeClass()
                .addClass("status processing")
                .html('<i class="fas fa-spinner fa-spin me-2"></i> Processing video...')
                .show();

            const formData = new FormData();
            formData.append("video", videoFile);

            fetch("/process_video", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError('processing-status', data.error);
                } else {
                    showSuccess('processing-status', data.message);

                    // Update results
                    $("#total-activities").text(data.activity_count);
                    $("#download-btn").attr("href", `/download_video/${data.output_filename}`);

                    $("#video-loading").show();
                    $("#video-container").show();

                    const videoUrl = `/processed_videos/${data.output_filename}`;
                    $("#video-player").attr("src", videoUrl);
                    $("#results-section").show();

                    setTimeout(() => {
                        const videoElement = $("#video-player")[0];

                        videoElement.oncanplay = function() {
                            $("#video-loading").hide();
                            const playPromise = videoElement.play();

                            if (playPromise !== undefined) {
                                playPromise.catch(error => {
                                    console.log("Autoplay prevented:", error);
                                    $("#play-overlay").show();
                                });
                            }
                        };

                        videoElement.onerror = function() {
                            $("#video-loading").hide();
                            showError('processing-status', 'Error playing video');
                            console.error("Video playback error:", videoElement.error);
                        };
                    }, 500);
                }
            })
            .catch(error => {
                showError('processing-status', error.message);
            });
        });

        // Manually play video if autoplay fails
        $("#play-overlay").click(function() {
            $(this).hide();
            $("#video-player")[0].play();
        });

        // Stop video feed when switching tabs
        $('#sourceTab a').on('shown.bs.tab', function(e) {
            if (currentSource) {
                stopVideoFeed();
            }
        });
    }

    // Initialize event handlers on page load
    setupEventListeners();
});
