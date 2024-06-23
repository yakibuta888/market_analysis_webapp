// src/vitest-setup.ts
import 'whatwg-fetch'; // fetch APIのモック
import '@testing-library/jest-dom'; // jest-domのマッチャーを追加

// canvas要素のモック
HTMLCanvasElement.prototype.getContext = (contextId: string) => {
  if (contextId === '2d') {
    return {
      // CanvasRenderingContext2Dのプロパティとメソッドをすべてモック
      canvas: document.createElement('canvas'),
      fillRect: () => {},
      clearRect: () => {},
      getImageData: (x: number, y: number, w: number, h: number) => ({
        data: new Uint8Array(w * h * 4)
      }),
      putImageData: () => {},
      createImageData: () => ([]),
      setTransform: () => {},
      drawImage: () => {},
      save: () => {},
      fillText: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      closePath: () => {},
      stroke: () => {},
      translate: () => {},
      scale: () => {},
      rotate: () => {},
      arc: () => {},
      fill: () => {},
      measureText: () => ({
        width: 0
      }),
      transform: () => {},
      rect: () => {},
      clip: () => {},
      // 追加のプロパティとメソッド
      globalAlpha: 1.0,
      globalCompositeOperation: 'source-over',
      imageSmoothingEnabled: true,
      imageSmoothingQuality: 'low',
      lineCap: 'butt',
      lineDashOffset: 0.0,
      lineJoin: 'miter',
      lineWidth: 1.0,
      miterLimit: 10.0,
      shadowBlur: 0,
      shadowColor: 'rgba(0, 0, 0, 0)',
      shadowOffsetX: 0,
      shadowOffsetY: 0,
      strokeStyle: '#000000',
      textAlign: 'start',
      textBaseline: 'alphabetic',
      direction: 'inherit',
      font: '10px sans-serif',
      filter: 'none',
      createLinearGradient: () => ({
        addColorStop: () => {}
      }),
      createPattern: () => null,
      createRadialGradient: () => ({
        addColorStop: () => {}
      }),
      getContextAttributes: () => null,
      getLineDash: () => [],
      isPointInPath: () => false,
      isPointInStroke: () => false,
      resetTransform: () => {},
      setLineDash: () => {},
      // その他のプロパティとメソッドを必要に応じて追加
    } as unknown as CanvasRenderingContext2D;
  }
  return null;
};
