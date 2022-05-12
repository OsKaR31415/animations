# animations

This is a python tool that allows to create animation on the command line.
It also allows to make presentations, with different slides, and the ability to go back and forward in the slides.

## Design Goals

 - Extensible
 - Simple and concise syntax
 - Lot of granularity (hability to work an any level)
 - Creation of an animation requires to only focus on what to draw, no perturbating elements

## How to achieve the design goals

### Extensibility
The tool will allow to create new animations, either via composing the shipped primitives, or by creating a new animation on your own, from scratch.
Since every animation in this tool is a generator of modifications to apply to the screen, an animation can do basically anything.

### Simplicity and concision of syntax
This tool has a particular syntax for _composing_ animations, that is to take two animations and to run them at the same time.
For instance, if `anim_a` and `anim_b` are two animations, then `anim_a >> anim_b` is also an animation that consists  of both animations running at the same time.
You certainly can compose more than two animations with : `anim_a >> anim_b >> anim_c >> anim_d ...`

This "composition" operator adds an animation **atop** the previous one. So, getting back to the example, the animation `anim_a >> anim_b`, is both animations composed, with `anim_b` **over** `anim_a`.
This is why the `>>` operator can also be called _over_.
Then, you won't have difficulties understanding what `<<` does : it is the _under_ operator, that adds an animation **under** the previous one.

The only thing to notice is that the precedence of these operators is left-to-right. So, for example, in this code : `anim_a >> anim_b >> anim_c << anim_under`, the animation `anim_under` is not only under `anim_c`, but actually under `anim_a >> anim_b >> anim_c`, so it is under all the other animations.

### Granularity
The system explained before (and that is explained further in the documentation) alows for granularity, thanks to primitives.
Primitives are only animations that are shipped with the tool. They allow to quickly define simple animations, like showing a text, draw a box, or making simple moving things.
By nature, they allow to create animations quickly, because you basically only need to compose then (with some settings to tell what text they have to show, or where they are).

But the user is also allowed to create animations from scratch. That allows to create extremely complex animation (basically anything that you would ever like to show on the terminal screen will be possible). For example, one could define the [Conway's Game of life](https://playgameoflife.com/) as an animation.

### Focus on only drawing
One important part of the design goals is that creating animation has to be done without worrying about any details.
No one likes when doing a simple thing requires thinking about tons of details that are useless to the real problem you want to solve.
So this tool tries to allow the creation of animations without worrying about useless details, even when you work on complex animations.
The synax with the operators `>>` and `<<` helps that purpose : you don't need to care yourself about how to put certain animations atop or under other ones.
You don't even need to how composing animations work !
To start creating animations, you just need to know some basic frame modifiers (functions that draw on the screen), and to know that an animation is made out of a function that yields frame modifiers.
You don't even need to know that, you could already make a lot of animations just using the primitives (so really, only understanding the _over_ and _under_ operators is required).





