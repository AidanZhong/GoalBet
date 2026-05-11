function extractVideoId(url: string): string | null {
    const match = url.match(
        /(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\s]{11})/
    );
    return match ? match[1] : null;
}

export default function YouTubeEmbed({url, className}: { url: string; className?: string }) {
    const videoId = extractVideoId(url);
    if (!videoId) return null;

    return (
        <div className={`aspect-video w-full rounded-xl overflow-hidden ${className ?? ""}`}>
            <iframe
                src={`https://www.youtube.com/embed/${videoId}`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-full"
            />
        </div>
    );
}
