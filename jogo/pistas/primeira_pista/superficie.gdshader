shader_type spatial;
render_mode diffuse_burley;
uniform vec4 cor : source_color = vec4(0.25, 0.32, 0.16, 1.0);
uniform float escala = 2.0;
uniform float variacao = 0.15;
varying vec3 mundo;
float ruido(vec2 p) {
	vec2 i = floor(p), f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(fract(sin(dot(i,vec2(127.1,311.7)))*43758.5453), fract(sin(dot(i+vec2(1,0),vec2(127.1,311.7)))*43758.5453),f.x), mix(fract(sin(dot(i+vec2(0,1),vec2(127.1,311.7)))*43758.5453),fract(sin(dot(i+vec2(1,1),vec2(127.1,311.7)))*43758.5453),f.x),f.y);
}
void vertex() { mundo = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	float n = ruido(mundo.xz * escala);
	ALBEDO = cor.rgb * (1.0 + (n - 0.5) * variacao);
	ROUGHNESS = 0.88 + 0.1 * n;
}
