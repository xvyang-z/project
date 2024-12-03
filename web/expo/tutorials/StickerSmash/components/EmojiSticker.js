import {Gesture} from 'react-native-gesture-handler';
import Animated, {useAnimatedStyle, useSharedValue, withSpring} from 'react-native-reanimated';
import {GestureDetector} from "react-native-gesture-handler/src/handlers/gestures/GestureDetector";
import {useEffect} from "react";

export function EmojiSticker({imageSize, stickerSource}) {

    // emoji 改变时重设大小
    useEffect(() => {
        scaleImage.value = imageSize
    }, [stickerSource])

    // 双击放大
    const scaleImage = useSharedValue(imageSize);
    const doubleTap = Gesture.Tap()
        .numberOfTaps(2)
        .onStart(() => {
            if (scaleImage.value !== imageSize * 4) {
                scaleImage.value = scaleImage.value * 2;
            }
        });
    const imageStyle = useAnimatedStyle(() => {
        return {
            width: withSpring(scaleImage.value),
            height: withSpring(scaleImage.value),
        };
    });

    // 拖动手势
    const translateX = useSharedValue(0);
    const translateY = useSharedValue(0);
    const drag = Gesture.Pan()
        .onChange((event) => {
            translateX.value += event.changeX;
            translateY.value += event.changeY;
        });
    const containerStyle = useAnimatedStyle(() => {
        return {
            transform: [
                {translateX: translateX.value,},
                {translateY: translateY.value,},
            ],
        };
    });


    return (
        <GestureDetector gesture={drag}>
            <Animated.View style={[containerStyle, {top: -50}]}>
                <GestureDetector gesture={doubleTap}>
                    <Animated.Image
                        source={stickerSource}
                        resizeMode="contain"
                        style={[imageStyle, {width: imageSize, height: imageSize}]}
                    />
                </GestureDetector>
            </Animated.View>
        </GestureDetector>
    );
}
