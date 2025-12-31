

import { useEffect, useRef, RefObject } from "react";


export function useAutoScroll<T>(
  dependencies: T[],
  enabled: boolean = true
): RefObject<HTMLDivElement> {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!enabled || !containerRef.current) return;

    const container = containerRef.current;
    const scrollToBottom = () => {
      container.scrollTop = container.scrollHeight;
    };

    // Use requestAnimationFrame to ensure DOM has updated
    requestAnimationFrame(() => {
      scrollToBottom();
    });
  }, dependencies);

  return containerRef;
}

