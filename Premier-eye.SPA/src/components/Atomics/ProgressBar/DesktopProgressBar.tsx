import React, { useEffect, useRef, useState } from 'react';
import { getDatetimeFromFilename } from '../../../services/DateFormatter';
import { IStepper } from '../../ImageViewer/ImageView/Steppers/IStepper';
import './DesktopProgressBar.pcss';

const toPixels = (num: number) => `${num}px`;

export const DesktopProgressBar = (props: IStepper) => {
    const [playerWidth, setPlayerWidth] = useState(600);
    const frameLength = playerWidth / props.images.length;

    const [frameTime, setFrameTime] = useState('');
    const borderWidth = 1;
    const ref = useRef<HTMLDivElement>(null);
    useEffect(() => {
        setPlayerWidth(ref.current !== null ? ref.current!.offsetWidth : 0);
    }, [ref.current]);

    const moving = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
        props.changeCurrentStep(frameIndex);
    };

    const onMouseEnter = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
        const src = props.images[frameIndex].src;
        const datetime = getDatetimeFromFilename(src);

        if (datetime !== null) {
            const time = `${datetime.getHours()}:${datetime.getMinutes()}:${datetime?.getSeconds()}`;
            setFrameTime(time);
        }
    };

    const getProgress = () => {
        // если шаг последний, то указатеь в конец
        // если первый, то указатель в начало
        // если нет, то в серидину длины текущего отрезка, а не в его начало
        if (props.currentStep == 0) return 0;
        if (props.currentStep === props.images.length - 1) return playerWidth - borderWidth * 2;
        return props.currentStep * frameLength + frameLength / 2;
    };

    return (
        <>
            <div ref={ref} className="outside" style={{ borderWidth: borderWidth }}>
                <div className="progress" style={{ width: toPixels(getProgress()) }} />
                {/*<div className="tip" >{frameTime}</div>*/}
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
