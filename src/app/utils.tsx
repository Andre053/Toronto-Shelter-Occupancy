import { AllStatsFsa, HeatmapData, StatsKey } from "@/types/types"

export const Section = ({children}: {children: React.ReactNode}) => (
    <div className="mt-[36px] mx-auto">
        {children}
    </div>
)

export const SectionHeading = ({children}: {children: React.ReactNode}) => (
    <h2 className="text-[26px] p-5 md:twt[36px] lg:txt[48px] font-bold text-center">
        {children}
    </h2>
)
export const SectionSubHeading = ({children}: {children: React.ReactNode}) => (
    <h2 className="text-[20px] md:twt[36px] lg:txt[48px] font-bold text-center">
        {children}
    </h2>
)
export const SectionContent = ({children}: {children: React.ReactNode}) => (
    <div className="text-[14px] leading-8 py-8 mx-auto max-w-2xl text-justify">
        {children}
    </div>
)
export const Link = ({url, children}: {url: string; children: React.ReactNode}) => (
    <a href={url} className="underline text-blue-800 hover:text-yellow-800">
        {children}
    </a>
)

export const setJsonData = async (jsonPath: string, setData: any) => {
    await fetch(jsonPath)
        .then(res => res.json())
        .then(data => {
            setData(data)
        })
        .catch((e: any) => console.log(e))
}

export const filterFsaStats = (fsaStats: AllStatsFsa[], stat: StatsKey) => {
    const heatmapData: HeatmapData = {
        statName: stat,
        statMax: 0,
        statMin: 10000,
        stats: {}
    }
    const statByFsa: any = {}
    fsaStats.forEach(v => {
        const curStat = v.STATS[stat]
        statByFsa[v.FSA] = curStat; // TODO: Type error, fix
        if (heatmapData.statMax < curStat) heatmapData.statMax = curStat;
        if (heatmapData.statMin > curStat) heatmapData.statMin = curStat;
    })
    heatmapData.stats = statByFsa;
    return heatmapData
}