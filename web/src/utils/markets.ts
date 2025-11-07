export type MarketsAny = any;

export function normalizeMarkets(markets: MarketsAny): {
    support: number;
    against: number;
    total: number;
} {
    if (!markets) return {support: 0, against: 0, total: 0};

    if (Array.isArray(markets)) {
        const support = Number(markets[0]) || 0;
        const against = Number(markets[1]) || 0;
        return {support, against, total: support + against};
    }

    if (typeof markets === "object") {
        const support = Number(markets.support) || 0;
        const against = Number(markets.against) || 0;
        const total = Number(markets.total ?? support + against) || support + against;
        return {
            support, against, total
        };
    }

    return {support: 0, against: 0, total: 0};
}