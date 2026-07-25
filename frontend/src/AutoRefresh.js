import { useEffect, useRef } from 'react';

function AutoRefresh({ onRefresh, interval = 300000 }) {
  const savedCallback = useRef();

  useEffect(() => {
    savedCallback.current = onRefresh;
  }, [onRefresh]);

  useEffect(() => {
    const tick = () => savedCallback.current();
    const timer = setInterval(tick, interval);
    return () => clearInterval(timer);
  }, [interval]);

  return null;
}

export default AutoRefresh;