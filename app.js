async function loadStories() {
    const container = document.getElementById("stories");

    try {
        const response = await fetch("stories.json", {
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error("Unable to load stories.");
        }

        const stories = await response.json();

        if (!Array.isArray(stories) || stories.length === 0) {
            throw new Error("No stories available.");
        }

        container.innerHTML = "";

        stories.slice(0, 10).forEach((story) => {
            const article = document.createElement("article");
            article.className = "story";

            const title = document.createElement("h2");
            title.className = "story-title";

            const link = document.createElement("a");
            link.href = story.link;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.textContent = story.title;

            title.appendChild(link);

            const date = document.createElement("p");
            date.className = "story-date";
            date.textContent = story.date;

            article.appendChild(title);
            article.appendChild(date);

            container.appendChild(article);
        });

    } catch (error) {
        container.innerHTML =
            '<p class="status">Unable to load stories.</p>';
    }
}

loadStories();
