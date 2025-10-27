'use client'
import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { DataPoint, GraphData } from "@/types/types";


type statKey = {
    [key: string]: string;
}

const graphStatKey: statKey = {
    'SERVICE_USER_COUNT': 'Service Users',
    'OCCUPIED_BEDS': 'Occupied Beds',
    'UNOCCUPIED_BEDS': 'Unoccupied Beds',
}

const capitalize = (val: string) => {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1)
}

const createTooltip = (tooltipId: string) => {
    return d3.select('body') 
        .append('div')
        .attr('id', tooltipId)
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('font-weight', 'bold')
        .style('background-color', 'white')
        .style('padding', '1px')
        .style('color', 'black')
        .style('border', 'solid')
        .style('z-index', 2)
        .style('opacity', 0.7)
}

// TODO: fix the type
const createCircle = (g: any, circleId: string) => {
    return g.append('circle')
        .attr('id', circleId)
        .attr('r', 0)
        .attr('fill', 'steelblue')
        .attr('opacity', 0.8)
        .style('stroke', 'white')
        .style('pointer-events', 'none');
}

type Props = {
    data: GraphData | null;
    stat: string;
    title: string;
}
export function LineChart({data, stat, title}: Props) {

    const width = 800;
    const height = 500;

    const margin = { 
        top: 70, 
        right: 100, 
        bottom: 75, 
        left: 50
    }

    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);
    const ttRef = useRef<HTMLDivElement | null>(null);

    const ttId = "tooltip-" + stat.replaceAll(' ', '-')
    const circleId = "circle-" + stat.replaceAll(' ', '-')
    const rectId = "rect-" + stat.replaceAll(' ', '-')

        //.attr('transform', `translate(${margin.left}, ${margin.top})`)

    useEffect(() => {
        if (!data) return; // wait until all are set  
        const dataPoints: DataPoint[] = data.dataPoints;
        dataPoints.forEach(dp => {
            dp.DATE = new Date(dp.DATE);
        })
            
        const yMax = data.max;
        const yMin = data.min;
        const dates = d3.extent(dataPoints, (d) => d.DATE);

        if (dates[0] == undefined) return;

        const svg = d3.select(svgRef.current)
            .attr('viewBox', [0, 0, width, height])
            .attr('border-weight', 'bold')

        const g = d3.select(gRef.current)
            .attr('transform', `translate(${margin.right}, ${margin.top})`) // move the g element by x, y\
            .attr('width', `${width-margin.right}`)
            .attr('height', `${height-margin.bottom-margin.top}`)

        g.selectAll('*').remove()

        const listeningRect = g.append('rect')
            .attr('id', rectId)
            .attr('width', width + 'px')
            .attr('height', height + 'px')
            .attr('opacity', 0)
            .attr('z-index', 1);

        const circle = createCircle(g, circleId)
        const tooltip = createTooltip(ttId)

        const xScale = d3.scaleTime()
            .range([0, width - margin.right - margin.left])
            .domain(dates)
        const yScale = d3.scaleLinear()
            .range([height-margin.top-margin.bottom, 0])
            .domain([0, yMax + 25]) 

        svg.selectAll('text').remove()
        svg.append('text')
            .style('fill', 'white')
            .attr('text-anchor', 'end')
            .attr("x", (width-margin.right-margin.left))
            .attr('y', margin.top/2)
            .style('font-size', '24px')
            .text(title)
        svg.append('text')
            .style('fill', 'white')
            .attr('text-anchor', 'end')
            .attr("x", (width)/2)
            .attr('y', height-(margin.bottom-10)/2)
            .text("Date")
        svg.append("text")
            .style('fill', 'white')
            .attr("text-anchor", "end")
            .attr("y", margin.right/4)
            .attr("x", -height/4)
            .attr("dy", "1.5em")
            .attr("transform", "rotate(-90)")
            .text(`${capitalize(data.timespan)} ${stat}`); // get title from backend
        
        const ticks = d3.timeMonth.every(6)

        g.append('g')
            .attr('transform', `translate(0,${height-margin.bottom-margin.top})`)
            .call(d3.axisBottom(xScale)
                .ticks(ticks))
        g.append('g')
            .call(d3.axisLeft(yScale))

        const line: any = d3.line()
            .x((d: any) => xScale(d.DATE))
            .y((d: any) => yScale(d.STAT))
        
        g.append('path')
            .datum(dataPoints)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2)
            .attr('d', (d: any) => {
                console.log({d}); // the whole data?
                return line(d);
            })
        
        listeningRect.on('mousemove', (e: any) => {
            const [xCoord] = d3.pointer(e) // values relative to the element
            const bisectDate = d3.bisector((d: DataPoint) => d.DATE).left

            const x0: any = xScale.invert(xCoord);
            const i = bisectDate(dataPoints, x0, 1);
            const d0: any = dataPoints[i];
            const d1: any = dataPoints[i-1];
            const d: DataPoint = x0 - d0.DATE > d1.DATE - x0 ? d1 : d0;
            const xPos = xScale(d.DATE); 
            const yPos = yScale(d.STAT);

            circle
                .attr('cx', xPos)
                .attr('cy', yPos)
                .transition()
                .duration(50)
                .attr('r', 5);

            // tooltip needs abs value does not account for scroll
            const scroll = window.scrollY
            const container = document.getElementById(rectId);
            if (!container) return;
            const containerDomRect = container.getBoundingClientRect();
            
            const xTooltip = xPos + containerDomRect.x
            const yTooltip = yPos + containerDomRect.y + scroll

            tooltip
                .style('left', `${xTooltip+10}px`)
                .style('top', `${yTooltip-30}px`)
                .text(`${d.DATE.toLocaleDateString()}\n\n${data.stat}: ${d.STAT}`);
        });
        listeningRect.on('mouseenter', () => {
            tooltip.style('visibility', 'visible')
            circle.style('visibility', 'visible')
        })
        listeningRect.on('mouseleave', () => {
            tooltip.style('visibility', 'hidden')
            circle.style('visibility', 'hidden')
        })
    }, [data]);

    return (
        <>
            <div id='chart-container' className='justify-center z-1 flex px-10 py-5'>
                <svg id='chart-svg' ref={svgRef} className="border border-5 border-gray-500 rounded-4xl p-5 text-white-400">
                    <g ref={gRef}>
                    </g>
                </svg>
            </div>            
        </>

    )
}