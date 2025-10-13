let currentReviewId = null;

// Load recent reviews on page load
document.addEventListener('DOMContentLoaded', function() {
    loadRecentReviews();
});

async function submitCode() {
    const fileInput = document.getElementById('fileInput');
    const filenameInput = document.getElementById('filenameInput');
    const codeInput = document.getElementById('codeInput');
    
    let filename = '';
    let content = '';
    
    // Check if file is uploaded
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        filename = file.name;
        content = await file.text();
    } else if (filenameInput.value.trim() && codeInput.value.trim()) {
        // Use text input
        filename = filenameInput.value.trim();
        content = codeInput.value.trim();
    } else {
        alert('Please either upload a file or provide both filename and code content.');
        return;
    }
    
    if (!content.trim()) {
        alert('Please provide code content to review.');
        return;
    }
    
    // Show loading modal
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();
    
    try {
        let response;
        
        if (fileInput.files.length > 0) {
            // Upload file
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            response = await fetch('/api/review', {
                method: 'POST',
                body: formData
            });
        } else {
            // Submit text
            response = await fetch('/api/review-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: filename,
                    content: content
                })
            });
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        displayReviewResults(result);
        currentReviewId = result.id;
        
        // Reload recent reviews
        loadRecentReviews();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error reviewing code: ' + error.message);
    } finally {
        loadingModal.hide();
    }
}

function displayReviewResults(review) {
    // Show results section
    document.getElementById('reviewResults').style.display = 'block';
    
    // Update scores
    updateScore('readabilityScore', review.readability_score);
    updateScore('modularityScore', review.modularity_score);
    updateScore('bugRiskScore', review.bug_risk_score);
    updateScore('overallScore', review.overall_score);
    
    // Update report
    document.getElementById('analysisReport').textContent = review.review_report;
    
    // Update suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    
    const suggestions = review.suggestions.split('\n').filter(s => s.trim());
    suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion.trim();
        suggestionsList.appendChild(li);
    });
    
    // Scroll to results
    document.getElementById('reviewResults').scrollIntoView({ behavior: 'smooth' });
}

function updateScore(elementId, score) {
    const element = document.getElementById(elementId);
    element.textContent = score.toFixed(1);
    
    // Add color class based on score
    element.className = 'score';
    if (score >= 8) {
        element.classList.add('excellent');
    } else if (score >= 6) {
        element.classList.add('good');
    } else if (score >= 4) {
        element.classList.add('average');
    } else {
        element.classList.add('poor');
    }
}

async function loadRecentReviews() {
    try {
        const response = await fetch('/api/reviews?limit=5');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reviews = await response.json();
        displayRecentReviews(reviews);
        
    } catch (error) {
        console.error('Error loading recent reviews:', error);
    }
}

function displayRecentReviews(reviews) {
    const container = document.getElementById('recentReviews');
    
    if (reviews.length === 0) {
        container.innerHTML = '<p class="text-muted">No recent reviews</p>';
        return;
    }
    
    container.innerHTML = '';
    
    reviews.forEach(review => {
        const item = document.createElement('div');
        item.className = 'recent-review-item';
        item.onclick = () => loadReview(review.id);
        
        const date = new Date(review.created_at).toLocaleDateString();
        
        item.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <div class="filename">${review.filename}</div>
                    <div class="date">${date}</div>
                </div>
                <div class="score">${review.overall_score.toFixed(1)}</div>
            </div>
        `;
        
        container.appendChild(item);
    });
}

async function loadReview(reviewId) {
    try {
        const response = await fetch(`/api/reviews/${reviewId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const review = await response.json();
        displayReviewResults(review);
        currentReviewId = reviewId;
        
    } catch (error) {
        console.error('Error loading review:', error);
        alert('Error loading review: ' + error.message);
    }
}

// Handle file input change
document.getElementById('fileInput').addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        document.getElementById('filenameInput').value = file.name;
        
        // Read and display file content
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('codeInput').value = e.target.result;
        };
        reader.readAsText(file);
    }
});

// Clear form function
function clearForm() {
    document.getElementById('fileInput').value = '';
    document.getElementById('filenameInput').value = '';
    document.getElementById('codeInput').value = '';
    document.getElementById('reviewResults').style.display = 'none';
    currentReviewId = null;
}
