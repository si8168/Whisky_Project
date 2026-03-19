// Function to show the survey ad
function showSurveyAd() {
    // 1. Check if the 'adShown' flag exists in this session
    const adShown = sessionStorage.getItem('adShown');

    // 2. Only show the ad if 'adShown' is NOT true
    if (!adShown) {
        const adModal = document.getElementById('survey-ad');
        if (adModal) {
            adModal.style.display = 'flex';
            // 3. Set the flag so it doesn't show again this visit
            sessionStorage.setItem('adShown', 'true');
        }
    }
}

// Start the 10-second timer
window.onload = function() {
    setTimeout(showSurveyAd, 10000); 
};

// Function to close the ad
function closeAd() {
    document.getElementById('survey-ad').style.display = 'none';
}



document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("homeModal");
    
    // Check if the user has already seen the ad this session
    if (!sessionStorage.getItem("adSeen")) {
        setTimeout(() => {
            modal.style.display = "flex";
        }, 1500); // Pops up after 1.5 seconds
    }

    window.closeModal = function() {
        modal.style.display = "none";
        sessionStorage.setItem("adSeen", "true");
    };

    document.querySelector(".close-modal").onclick = closeModal;
});

