
<div class="no-post-container">
    <div class="no-post">
        <div class="no-post-icon">
            <i class="fas fa-folder-open"></i>
        </div>
        <h4>No data Available</h4>
        <p>Try searching for a different keyword or filter.</p>
    </div>
</div>


<style>
    .no-post-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 300px;
        text-align: center;
    }

    .no-post {
        animation: fadeIn 1s ease-in-out;
        color: #555;
    }

    .no-post-icon {
        font-size: 4rem;
        color: #aaa;
        animation: bounce 2s infinite;
    }

    .no-post h4 {
        margin-top: 1rem;
        font-weight: bold;
        font-size: 1.5rem;
        color: #333;
    }

    .no-post p {
        margin-top: 0.5rem;
        color: #666;
        font-size: 1rem;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
</style>