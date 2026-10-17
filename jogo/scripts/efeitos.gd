class_name Efeitos
extends RefCounted
## Efeitos visuais curtos criados na hora e removidos sozinhos.

static var _processo: ParticleProcessMaterial
static var _malha: Mesh


## Faíscas saindo do ponto de contato, abertas em leque em torno da normal.
## intensidade: velocidade do choque em m/s.
static func faiscas(pai: Node, ponto: Vector3, normal: Vector3, intensidade: float) -> void:
	if pai == null or intensidade < 1.5:
		return
	if _processo == null:
		_preparar()
	var p := GPUParticles3D.new()
	p.one_shot = true
	p.explosiveness = 0.95
	p.lifetime = 0.6
	p.amount = clampi(roundi(intensidade * 3.0), 6, 48)
	var processo := _processo.duplicate() as ParticleProcessMaterial
	processo.direction = normal.lerp(Vector3.UP, 0.35).normalized()
	p.process_material = processo
	p.draw_pass_1 = _malha
	p.local_coords = false
	pai.add_child(p)
	p.global_position = ponto
	p.emitting = true
	p.finished.connect(p.queue_free)


static func _preparar() -> void:
	_processo = ParticleProcessMaterial.new()
	_processo.spread = 60.0
	_processo.initial_velocity_min = 3.0
	_processo.initial_velocity_max = 9.0
	_processo.gravity = Vector3(0, -14, 0)
	_processo.damping_min = 1.0
	_processo.damping_max = 3.0
	_processo.scale_min = 0.6
	_processo.scale_max = 1.2
	var cores := Gradient.new()
	cores.set_color(0, Color(1.0, 0.95, 0.6))
	cores.set_color(1, Color(1.0, 0.35, 0.05, 0.0))
	var rampa := GradientTexture1D.new()
	rampa.gradient = cores
	_processo.color_ramp = rampa

	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.vertex_color_use_as_albedo = true
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.emission_enabled = true
	material.emission = Color(1.0, 0.6, 0.2)
	material.emission_energy_multiplier = 3.0
	var caixa := BoxMesh.new()
	caixa.size = Vector3(0.09, 0.09, 0.09)
	caixa.material = material
	_malha = caixa
