import { createDraggable, createTimeline, stagger, utils, splitText, spring, waapi } from '/static/js/anime.js';

// with a timeline

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
	filter: 'drop-shadow(0px 0px 4px var(--yellow))',
	ease: 'inOut',
	duration: 400,
	delay: stagger(400),
});

const animateSun = waapi.animate("#sun", {
	transform: {
		to: 'scaleX(0.95) scaleY(1.1)',
		duration: 500
	},
	alternate: true,
	duration: 100,
	ease: spring({ bounce: .35 }),
	filter: 'drop-shadow(0px 0px 4px var(--yellow))',
});

// bah jcomprends pas pk sun mets tant de temps

createTimeline({
	loop: true,
	alternate: true,
	delay: 1000,
	// attention pas dans waapi
	loopDelay: 2000
})
.sync(animateChars, 0)
.sync(animateWords, animateChars.duration)
.sync(animateSun, animateChars.duration)
.init();

// simple waapi

waapi.animate("#supporters ul li", {
	'y': {
		to: -2
	},
	duration: 1000,
	loop: true,
	alternate: true,
	delay: stagger(400),
})

// let's try cartoon sticker effect

const wiggle = waapi.animate("#avatar", {
	'filter': {
		to: 'drop-shadow(0px 0px 4px var(--yellow))'
	},
	duration: 200,
	loop: true,
	alternate: true,
	autoplay: false,
})

// ça marche mais je le mets pas
// oh ptdr si quand je drag l'avatar
// ... non ça combote pas bien

// un custom event pour voir

const event = new CustomEvent('avatar', {
	bubbles: true
});

// and draggable avatar

const avatar = createDraggable('#avatar', {
	container: 'body',
	containerPadding: [0, 20, 0, 0],
	containerFriction: 1,
	// besoin des deux quand même
	// ça marche bien, ça peut même se snap ! la dingz
	onGrab: () => document.dispatchEvent(event),
	onDrag: () => wiggle.restart(),
	onRelease: () => {
		wiggle.pause();
		wiggle.seek(0);
	},
});

console.log(avatar)

// ça marche nickel pour reset l'anim comme ça

// bon bah jeu de cartes go
// et je vais ptet même utiliser layout pour les cartes

// on révise export

window.show = function (el) {
	waapi.animate(el, {
		opacity: 1,
		duration: 200,
	});
}
