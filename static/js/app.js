// Main application JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const textInput = document.getElementById('textInput');
    const resultsSection = document.getElementById('resultsSection');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Event Listeners
    analyzeBtn.addEventListener('click', handleAnalysis);
    textInput.addEventListener('input', validateInput);

    async function handleAnalysis() {
        const text = textInput.value.trim();
        if (!text) {
            showError('Please enter some text to analyze');
            return;
        }

        try {
            showLoading(true);
            const results = await analyzeText(text);
            displayResults(results);
            showLoading(false);
            resultsSection.classList.remove('hidden');
            resultsSection.classList.add('fade-in');
        } catch (error) {
            showError('Analysis failed: ' + error.message);
            showLoading(false);
        }
    }

    async function analyzeText(text) {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error('Analysis request failed');
        }

        return await response.json();
    }

    function displayResults(results) {
        displayPolarity(results.polarity);
        displayConcerns(results.concerns);
        displayKeywords(results.keywords);
        displayIntensity(results.intensity);
        displayTimeline(results.timeline);
    }

    function displayPolarity(polarity) {
        const polarityValue = document.getElementById('polarityValue');
        const polarityBar = document.getElementById('polarityBar');

        polarityValue.textContent = polarity.label;
        polarityBar.style.width = `${polarity.score * 100}%`;

        // Update color based on polarity
        const colors = {
            positive: 'bg-green-500',
            negative: 'bg-red-500',
            neutral: 'bg-blue-500'
        };

        polarityBar.className = `h-2.5 rounded-full transition-all duration-500 ${colors[polarity.label]}`;
    }

    function displayConcerns(concerns) {
        const concernsResult = document.getElementById('concernsResult');
        concernsResult.innerHTML = '';

        if (concerns.primary_concern) {
            const primaryConcern = document.createElement('div');
            primaryConcern.className = 'mb-4';
            primaryConcern.innerHTML = `
                <div class="text-lg font-semibold mb-2">Primary Concern</div>
                <div class="bg-blue-100 text-blue-800 px-4 py-2 rounded-lg">
                    ${concerns.primary_concern}
                    <div class="text-sm text-blue-600 mt-1">
                        Confidence: ${(concerns.confidence * 100).toFixed(1)}%
                    </div>
                </div>
            `;
            concernsResult.appendChild(primaryConcern);
        }

        if (concerns.additional_concerns && concerns.additional_concerns.length > 0) {
            const additionalConcerns = document.createElement('div');
            additionalConcerns.innerHTML = `
                <div class="text-lg font-semibold mb-2">Additional Concerns</div>
                <div class="flex flex-wrap gap-2">
                    ${concerns.additional_concerns.map(concern => `
                        <span class="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">
                            ${concern}
                        </span>
                    `).join('')}
                </div>
            `;
            concernsResult.appendChild(additionalConcerns);
        }
    }

    function displayKeywords(keywords) {
        const keywordsResult = document.getElementById('keywordsResult');
        keywordsResult.innerHTML = '';

        keywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            keywordsResult.appendChild(tag);
        });
    }

    function displayIntensity(intensity) {
        const intensityBar = document.getElementById('intensityBar');
        const aspectIntensities = document.getElementById('aspectIntensities');
        
        // Update overall intensity
        intensityBar.style.width = `${(intensity.overall_intensity / 10) * 100}%`;
        
        // Update aspect intensities
        aspectIntensities.innerHTML = '';
        Object.entries(intensity.aspects).forEach(([aspect, score]) => {
            const aspectDiv = document.createElement('div');
            aspectDiv.className = 'mb-3';
            aspectDiv.innerHTML = `
                <div class="flex justify-between mb-1">
                    <span class="text-gray-600">${aspect}</span>
                    <span class="font-medium">${score}/10</span>
                </div>
                <div class="intensity-bar">
                    <div class="intensity-bar-fill ${getIntensityClass(score)}"
                         style="width: ${(score / 10) * 100}%"></div>
                </div>
            `;
            aspectIntensities.appendChild(aspectDiv);
        });
    }

    function displayTimeline(timeline) {
        const timelineResult = document.getElementById('timelineResult');
        timelineResult.innerHTML = `
            <div class="mb-4">
                <span class="font-semibold">Duration:</span> ${timeline.duration}
            </div>
            <div class="mb-4">
                <span class="font-semibold">Progression:</span> ${timeline.progression}
            </div>
            <div class="mb-4">
                <span class="font-semibold">Frequency:</span> ${timeline.frequency}
            </div>
        `;

        if (timeline.temporal_indicators.length > 0) {
            const indicators = document.createElement('div');
            indicators.innerHTML = `
                <div class="font-semibold mb-2">Temporal Indicators:</div>
                <div class="flex flex-wrap gap-2">
                    ${timeline.temporal_indicators.map(indicator => `
                        <span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                            ${indicator}
                        </span>
                    `).join('')}
                </div>
            `;
            timelineResult.appendChild(indicators);
        }
    }

    function getIntensityClass(score) {
        if (score <= 3) return 'intensity-low';
        if (score <= 7) return 'intensity-medium';
        return 'intensity-high';
    }

    function validateInput() {
        const text = textInput.value.trim();
        analyzeBtn.disabled = !text;
        analyzeBtn.className = text 
            ? 'bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors'
            : 'bg-gray-300 text-gray-500 px-6 py-2 rounded-lg cursor-not-allowed';
    }

    function showLoading(show) {
        loadingIndicator.className = show 
            ? 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center'
            : 'hidden';
    }

    function showError(message) {
        // Create and show error toast
        const toast = document.createElement('div');
        toast.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg fade-in';
        toast.textContent = message;
        document.body.appendChild(toast);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
});