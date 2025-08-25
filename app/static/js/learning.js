// Learning materials JavaScript

async function loadLearningTopic(topic) {
    try {
        const topicBtn = document.querySelector(`[onclick="loadLearningTopic('${topic}')"]`);
        const originalHtml = topicBtn.innerHTML;
        
        // Show loading state
        topicBtn.innerHTML = '<div class="d-flex justify-content-between align-items-center"><div><strong>Loading...</strong></div><i class="fas fa-spinner fa-spin"></i></div>';
        
        const response = await fetch('/api/generate-learning-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });
        
        const result = await response.json();
        
        if (result.error) {
            showError(result.error);
        } else {
            showLearningContent({
                text: result.content,
                format: result.format || 'text'
            });
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        // Restore original button state
        if (topicBtn) {
            topicBtn.innerHTML = originalHtml;
        }
    }
}

function showLearningContent(content) {
    const contentArea = document.getElementById('learningContentArea');
    
    // Show the content area if hidden
    contentArea.style.display = 'block';
    
    // Scroll to content area
    contentArea.scrollIntoView({ behavior: 'smooth' });
    
    // Clear previous content
    const contentContainer = document.getElementById('learningContent');
    
    // Render content based on format
    if (typeof content === 'object' && content.text && content.format === 'markdown') {
        contentContainer.innerHTML = `<div class="markdown-content">${marked.parse(content.text)}</div>`;
    } else if (typeof content === 'string') {
        contentContainer.innerHTML = `<div class="prose">${content.replace(/\n/g, '<br>')}</div>`;
    }
}

function showError(error) {
    const contentArea = document.getElementById('learningContentArea');
    const contentContainer = document.getElementById('learningContent');
    
    contentArea.style.display = 'block';
    contentContainer.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i> <strong>Error:</strong> ${error}
        </div>
    `;
}
