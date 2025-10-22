import React, { useRef, useEffect, useState, useCallback } from 'react';

const STORAGE_KEY = 'drawingCanvas:dataURL';

function DrawingCanvas() {
  const canvasRef = useRef(null);
  const ctxRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const lastPointRef = useRef({ x: 0, y: 0 });

  // Set up canvas (including HiDPI scaling) and restore saved image if present
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const dpr = window.devicePixelRatio || 1;
    const cssWidth = 800;
    const cssHeight = 600;

    // Set the display size (css) and the internal size (pixels)
    canvas.style.width = `${cssWidth}px`;
    canvas.style.height = `${cssHeight}px`;
    canvas.width = Math.floor(cssWidth * dpr);
    canvas.height = Math.floor(cssHeight * dpr);

    const ctx = canvas.getContext('2d');
    ctxRef.current = ctx;

    // Normalize drawing units to CSS pixels
    ctx.scale(dpr, dpr);
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    // Restore from localStorage if available
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const img = new Image();
      img.onload = () => {
        // drawImage expects CSS pixel coordinates after scaling
        ctx.drawImage(img, 0, 0, cssWidth, cssHeight);
      };
      img.src = saved;
    }
  }, []);

  const saveCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    try {
      const dataURL = canvas.toDataURL('image/png');
      localStorage.setItem(STORAGE_KEY, dataURL);
    } catch {
      // Ignore quota or security errors (e.g., in private mode)
    }
  }, []);

  const getOffset = (e) => {
    // Supports mouse & touch
    if ('nativeEvent' in e && e.nativeEvent.touches && e.nativeEvent.touches[0]) {
      const rect = canvasRef.current.getBoundingClientRect();
      const t = e.nativeEvent.touches[0];
      return { x: t.clientX - rect.left, y: t.clientY - rect.top };
    }
    const { offsetX, offsetY } = e.nativeEvent;
    return { x: offsetX, y: offsetY };
  };

  const startDrawing = (e) => {
    const { x, y } = getOffset(e);
    setIsDrawing(true);
    lastPointRef.current = { x, y };
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const ctx = ctxRef.current;
    if (!ctx) return;

    const { x, y } = getOffset(e);
    const { x: lx, y: ly } = lastPointRef.current;

    ctx.beginPath();
    ctx.moveTo(lx, ly);
    ctx.lineTo(x, y);
    ctx.stroke();

    lastPointRef.current = { x, y };
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    saveCanvas(); // Save after each completed stroke
  };

  // Optional: Save before tab closes (extra safety)
  useEffect(() => {
    const handler = () => saveCanvas();
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [saveCanvas]);

  return (
    <canvas
      ref={canvasRef}
      onMouseDown={startDrawing}
      onMouseMove={draw}
      onMouseUp={stopDrawing}
      onMouseLeave={stopDrawing}
      onTouchStart={startDrawing}
      onTouchMove={(e) => { e.preventDefault(); draw(e); }} // prevent page scroll while drawing
      onTouchEnd={stopDrawing}
      style={{ border: '1px solid black', touchAction: 'none', display: 'block' }}
    />
  );
}

export default DrawingCanvas;
