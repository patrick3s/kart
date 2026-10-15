shader_type spatial;
// Piso quadriculado em coordenadas do mundo, com filtragem para não cintilar ao longe.

uniform vec4 cor_a : source_color = vec4(0.93, 0.93, 0.9, 1.0);
uniform vec4 cor_b : source_color = vec4(0.16, 0.18, 0.23, 1.0);
uniform float tamanho = 2.0;

varying vec3 posicao_mundo;

void vertex() {
	posicao_mundo = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	vec2 p = posicao_mundo.xz / tamanho;
	vec2 w = fwidth(p) + 0.0001;
	vec2 i = 2.0 * (abs(fract((p - 0.5 * w) * 0.5) - 0.5) - abs(fract((p + 0.5 * w) * 0.5) - 0.5)) / w;
	float xadrez = 0.5 - 0.5 * i.x * i.y;
	ALBEDO = mix(cor_a.rgb, cor_b.rgb, xadrez);
	ROUGHNESS = 0.85;
}
