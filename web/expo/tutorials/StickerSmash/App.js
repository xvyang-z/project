import {StatusBar} from 'expo-status-bar';
import {StyleSheet, View, Platform} from 'react-native';
import {ImageViewer} from "./components/ImageViewer";
import {Button} from './components/Button'
import * as ImagePicker from 'expo-image-picker';
import {useRef, useState} from "react";
import {CircleButton} from './components/CircleButton';
import {IconButton} from './components/IconButton';
import {EmojiPicker} from "./components/EmojiPicker";
import EmojiList from "./components/EmojiList";
import {EmojiSticker} from "./components/EmojiSticker";
import {GestureHandlerRootView} from "react-native-gesture-handler";
import * as MediaLibrary from 'expo-media-library';
import {captureRef} from "react-native-view-shot";
import domtoimage from 'dom-to-image';

export default function App() {
    const [status, requestPermission] = MediaLibrary.usePermissions();
    if (status === null) {
        requestPermission();
    }

    const imageRef = useRef();
    const [pickedEmoji, setPickedEmoji] = useState(null);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [showAppOptions, setShowAppOptions] = useState(false);
    const [selectedImage, setSelectedImage] = useState(null);


    const pickImageAsync = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
            allowsEditing: true,
            quality: 1,
        });
        if (!result.canceled) {
            setSelectedImage(result.assets[0]);
            setShowAppOptions(true);
            console.log(result);
        } else {
            alert('You did not select any image.');
        }
    };
    const onReset = () => {
        setShowAppOptions(false);
    };

    const onAddSticker = () => {
        setIsModalVisible(true);
    };

    const onModalClose = () => {
        setIsModalVisible(false);
    };

    const onSaveImageAsync = async () => {
        if (Platform.OS !== 'web') {
            try {
                const localUri = await captureRef(imageRef, {
                    height: 440,
                    quality: 1,
                });
                await MediaLibrary.saveToLibraryAsync(localUri);
                if (localUri) {
                    alert('Saved!');
                }
            } catch (e) {
                console.log(e);
            }
        } else {
            try {
                const dataUrl = await domtoimage.toJpeg(imageRef.current, {
                    quality: 0.95,
                    width: 320,
                    height: 440,
                });

                let link = document.createElement('a');
                link.download = 'sticker-smash.jpeg';
                link.href = dataUrl;
                link.click();
            } catch (e) {
                console.log(e);
            }
        }
    };

    const new_Size = selectedImage? scaleTo400x400({
        originalWidth: selectedImage.width,
        originalHeight: selectedImage.height,
    }): {}

    const imageSizestyle = StyleSheet.create({
        image: {
            ...new_Size,
            overflow: "hidden"
        }
    })

    return (
        <GestureHandlerRootView style={styles.container}>
            <View style={styles.imageContainer}>
                <View ref={imageRef} collapsable={false} style={imageSizestyle.image}>
                    <ImageViewer assets={selectedImage} imageSizestyle={imageSizestyle.image}></ImageViewer>
                    {pickedEmoji && <EmojiSticker imageSize={40} stickerSource={pickedEmoji}/>}
                </View>
            </View>

            {showAppOptions ? (
                <View style={styles.optionsContainer}>
                    <View style={styles.optionsRow}>
                        <IconButton icon="refresh" label="Reset" onPress={onReset}/>
                        <CircleButton onPress={onAddSticker}/>
                        <IconButton icon="save-alt" label="Save" onPress={onSaveImageAsync}/>
                    </View>
                </View>
            ) : (
                <View style={styles.footerContainer}>
                    <Button label="Choose a photo" theme={'primary'} onPress={pickImageAsync}/>
                    <Button label="Use this photo" onPress={() => setShowAppOptions(true)}/>
                </View>
            )}

            <EmojiPicker isVisible={isModalVisible} onClose={onModalClose}>
                <EmojiList onSelect={setPickedEmoji} onCloseModal={onModalClose}/>
            </EmojiPicker>

            <StatusBar style="light"/>

        </GestureHandlerRootView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#25292e',
        alignItems: 'center',
        justifyContent: 'center',
    },
    imageContainer: {
        flex: 3,
        paddingTop: 58,
    },
    footerContainer: {
        flex: 1,
        alignItems: 'center',
    },
    optionsContainer: {
        position: 'absolute',
        bottom: 80,
    },
    optionsRow: {
        alignItems: 'center',
        flexDirection: 'row',
    },
});

function scaleTo400x400({originalWidth, originalHeight}) {
    const targetSize = 380;

    // 计算宽高比
    const aspectRatio = originalWidth / originalHeight;

    // 如果宽度和高度都在400x400范围内，则无需缩放
    if (originalWidth <= targetSize && originalHeight <= targetSize) {
        return {
            width: originalWidth,
            height: originalHeight
        };
    }

    // 根据宽高比缩放
    if (aspectRatio > 1) {
        // 宽度大于高度
        return {
            width: targetSize,
            height: targetSize / aspectRatio
        };
    } else {
        // 高度大于宽度
        return {
            width: targetSize * aspectRatio,
            height: targetSize
        };
    }
}
