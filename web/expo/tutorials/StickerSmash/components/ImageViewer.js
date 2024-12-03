import {Image} from 'react-native';

export function ImageViewer({assets, imageSizestyle}) {
    if (!assets) {
        return <Image></Image>
    }

    const imageSource = assets ? {uri: assets.uri} : null;

    return <Image source={imageSource} style={imageSizestyle}></Image>
}

