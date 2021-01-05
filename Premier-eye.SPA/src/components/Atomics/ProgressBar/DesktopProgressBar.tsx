import React, { useEffect, useRef, useState } from 'react';
import { range } from '../../../services/utils';
import { IStepper } from '../../ImageViewer/ImageView/Steppers/IStepper';
import './DesktopProgressBar.pcss';
import {getDatetimeFromFilename} from "../../../services/DateFormatter";

const toPixels = (num: number) => `${num}px`;

export const DesktopProgressBar = (props: IStepper) => {
    const [playerWidth, setPlayerWidth] = useState(600);
    const frameLength = playerWidth / props.images.length;

    const [frameTime, setFrameTime] = useState('');

    const ref = useRef<HTMLDivElement>(null);
    useEffect(() => {
        setPlayerWidth(ref.current !== null ? ref.current!.offsetWidth : 0);
    }, [ref.current]);

    const moving = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
        props.changeCurrentStep(frameIndex);
    };

    const onMouseEnter = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {

        const src = props.images[frameIndex].src
        const datetime = getDatetimeFromFilename(src);
        if (datetime !== null) {
            const time = `${datetime.getHours()}:${datetime.getMinutes()}:${datetime?.getSeconds()}`;
            setFrameTime(time);
        }

    };

    return (
        <>
            <div ref={ref} className="outside">

                <div className="progress" style={{ width: toPixels(props.currentStep * frameLength) }} />
                <div className="pointsContainer">
                    {props.images.map((empty, i) => (
                        <div
                            key={empty.id}
                            className="inside"
                            onMouseEnter={onMouseEnter(i)}
                            style={{ width: frameLength }}
                            onClick={moving(parseInt(empty.id))}
                        />
                    ))}
                </div>
            </div>
        </>
    );
};
