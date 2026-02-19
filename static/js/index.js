import { createTimeline, stagger, utils, splitText, waapi } from '/static/js/anime.js';

const { words, chars } = splitText("#welcome", { chars: true });

const animateChars = waapi.animate(chars, {
  y: '-5px',
  rotate: 5,
  ease: 'out',
  duration: 300,
  delay: stagger(120),
});

const animateWords = waapi.animate(words, {
  color: 'var(--yellow)',
  ease: 'inOut',
  duration: 400,
  delay: stagger(400),
});

createTimeline({
  loop: true,
  alternate: true,
  delay: 200,
  loopDelay: 1000,
})
.sync(animateChars, 0)
.sync(animateWords, animateChars.duration)
.init();
