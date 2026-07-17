const API = "http://127.0.0.1:8000";

const analyzeBtn = document.getElementById("analyzeBtn");
const reviewInput = document.getElementById("reviewInput");

const sentiment = document.getElementById("sentiment");
const confidence = document.getElementById("confidence");
const fake = document.getElementById("fake");

const totalReviews = document.getElementById("totalReviews");
const realReviews = document.getElementById("realReviews");
const fakeReviews = document.getElementById("fakeReviews");

const historyContainer = document.getElementById("historyContainer");
const searchBox = document.getElementById("searchBox");

let reviews = [];
let sentimentChart;
let fakeChart;

async function loadReviews(){
    const response = await fetch(`${API}/reviews`);
    reviews = await response.json();

    displayReviews(reviews);
    updateStats(reviews);
}

function updateStats(data){
    totalReviews.textContent = data.length;

    const genuine = data.filter(review => !review.fake).length;
    const fakeCount = data.filter(review => review.fake).length;
    const positive = data.filter(review => review.sentiment === "Positive").length;
    const negative = data.filter(review => review.sentiment === "Negative").length;

    realReviews.textContent = genuine;
    fakeReviews.textContent = fakeCount;

    drawCharts(positive, negative, genuine, fakeCount);
}

function drawCharts(positive, negative, genuine, fakeCount){
    if(sentimentChart){
        sentimentChart.destroy();
    }

    if(fakeChart){
        fakeChart.destroy();
    }

    const sharedOptions = {
        responsive:true,
        maintainAspectRatio:false,
        cutout:"62%",
        plugins:{
            legend:{
                position:"bottom",
                labels:{
                    color:"#cbd5e1",
                    boxWidth:12,
                    boxHeight:12,
                    padding:18,
                    font:{
                        family:"Inter",
                        size:13,
                        weight:"700"
                    }
                }
            }
        }
    };

    sentimentChart = new Chart(
        document.getElementById("sentimentChart"),
        {
            type:"doughnut",
            data:{
                labels:["Positive","Negative"],
                datasets:[{
                    data:[positive,negative],
                    backgroundColor:["#22c55e","#ef4444"],
                    borderColor:"#101725",
                    borderWidth:4,
                    hoverOffset:8
                }]
            },
            options:sharedOptions
        }
    );

    fakeChart = new Chart(
        document.getElementById("fakeChart"),
        {
            type:"doughnut",
            data:{
                labels:["Genuine","Fake"],
                datasets:[{
                    data:[genuine,fakeCount],
                    backgroundColor:["#38bdf8","#f59e0b"],
                    borderColor:"#101725",
                    borderWidth:4,
                    hoverOffset:8
                }]
            },
            options:sharedOptions
        }
    );
}

function displayReviews(data){
    historyContainer.innerHTML = "";

    if(data.length === 0){
        historyContainer.innerHTML = `
            <div class="empty-state">
                No reviews yet. Analyze a customer review to build your dashboard.
            </div>
        `;
        return;
    }

    [...data].reverse().forEach(review => {
        const card = document.createElement("article");
        const sentimentClass = review.sentiment === "Positive" ? "badge-positive" : "badge-negative";
        const authenticityClass = review.fake ? "badge-fake" : "badge-genuine";
        const authenticityText = review.fake ? "Fake Review" : "Genuine Review";
        const authenticityIcon = review.fake ? "fa-triangle-exclamation" : "fa-circle-check";

        card.className = "review-card";
        card.innerHTML = `
            <h3>${review.review}</h3>

            <div class="review-meta">
                <span class="badge ${sentimentClass}">
                    <i class="fa-solid fa-face-smile"></i>
                    ${review.sentiment}
                </span>

                <span class="badge badge-confidence">
                    <i class="fa-solid fa-chart-line"></i>
                    ${(review.confidence * 100).toFixed(2)}%
                </span>

                <span class="badge ${authenticityClass}">
                    <i class="fa-solid ${authenticityIcon}"></i>
                    ${authenticityText}
                </span>
            </div>
        `;

        historyContainer.appendChild(card);
    });
}

analyzeBtn.onclick = async () => {
    const text = reviewInput.value.trim();

    if(text === ""){
        alert("Please enter a review.");
        return;
    }

    analyzeBtn.innerHTML = `
        <div class="loading">
            <div></div>
            <div></div>
            <div></div>
        </div>
    `;

    const response = await fetch(`${API}/analyze`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            review:text
        })
    });

    const data = await response.json();

    sentiment.textContent = data.sentiment;
    confidence.textContent = `${(data.confidence * 100).toFixed(2)}%`;
    fake.textContent = data.fake ? "Fake Review" : "Genuine";

    analyzeBtn.innerHTML = `
        <i class="fa-solid fa-wand-magic-sparkles"></i>
        Analyze with AI
    `;

    reviewInput.value = "";
    loadReviews();
};

searchBox.addEventListener("input",() => {
    const keyword = searchBox.value.toLowerCase();
    const filtered = reviews.filter(review =>
        review.review.toLowerCase().includes(keyword)
    );

    displayReviews(filtered);
});

loadReviews();
