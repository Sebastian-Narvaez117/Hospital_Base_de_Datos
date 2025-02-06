from flask import  Blueprint, render_template, request, redirect,flash, url_for
from models import  Citas, Factura, HistorialMedico, Medico, Paciente, Tratamiento
from app import db

router2 = Blueprint('router2', __name__)


@router2.route('/register/medicos', methods=['GET', 'POST'])
def register_medicos():
    citas= Citas.query.all()
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            especialidad = request.form['especialidad']
            correo = request.form['correo']
            idCita = request.form['idCita']

            if not nombre or not apellido or not especialidad or not correo:
                flash('Todos los campos son requeridos', 'warning')
                return redirect(url_for('router2.register_medicos'))

            # Verificar si el correo ya está registrado
            existing_medico = Medico.query.filter_by(correo=correo).first()
            if existing_medico:
                flash('El correo ya está registrado', 'error')
                return redirect(url_for('router2.register_medicos'))

            medico = Medico(
                nombre=nombre,
                apellido=apellido,
                especialidad=especialidad,
                correo=correo,
                idCita=idCita
            )

            db.session.add(medico)
            db.session.commit()
            flash('Médico registrado correctamente', 'success')
            return redirect(url_for('router2.list_medicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el médico: ', 'error')
            return redirect(url_for('router2.register_medicos'))
    
    return render_template('/Medico/registro.html', citas=citas)

@router2.route('/list/medicos')
def list_medicos():
    medicos = Medico.query.all()
    citas = Citas.query.all()
    return render_template('/Medico/lista.html', medicos=medicos, citas=citas)


@router2.route('/edit/medicos/<int:id>', methods=['GET', 'POST'])
def edit_medicos(id):
    medico = Medico.query.get(id)
    citas = Citas.query.all()
    if request.method == 'POST':
        try:
            medico.nombre = request.form['nombre']
            medico.apellido = request.form['apellido']
            medico.especialidad = request.form['especialidad']
            medico.correo = request.form['correo']
            medico.idCita = request.form['idCita']

            db.session.commit()
            flash('Médico actualizado correctamente', 'success')
            return redirect(url_for('router2.list_medicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el médico: {str(e)}', 'error')
            return redirect(url_for('router2.edit_medicos', id=id))
    return render_template('/Medico/editar.html', medico=medico, citas=citas)



@router2.route('/delete/medicos/<int:id>', methods=['GET'])
def delete_medicos(id):
    try:
        medico = Medico.query.get_or_404(id)
        db.session.delete(medico)
        db.session.commit()
        flash('Médico eliminado correctamente', 'success')
        return redirect(url_for('router2.list_medicos'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el médico: {str(e)}', 'error')
        return redirect(url_for('router2.register_medicos'))

















@router2.route('/register/historial', methods=['GET', 'POST'])
def register_historial():
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            diagnostico = request.form['diagnostico']
            observaciones = request.form['observaciones']
            idPaciente = request.form['idPaciente']

            if not fecha or not diagnostico or not observaciones:
                flash('Todos los campos son requeridos', 'warning')
                return redirect(url_for('router2.register_historial'))

            historial = HistorialMedico(
                fecha=fecha,
                diagnostico=diagnostico,
                observaciones=observaciones,
                idPaciente=idPaciente
            )

            db.session.add(historial)
            db.session.commit()
            flash('Historial registrado correctamente', 'success')
            return redirect(url_for('router2.list_historial'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el historial', 'error')
            return redirect(url_for('router2.register_historial'))
    return render_template('/Historial/registro.html', pacientes=pacientes)


@router2.route('/list/historial')
def list_historial():
    historiales = HistorialMedico.query.all()
    pacientes = Paciente.query.all()
    return render_template('/Historial/lista.html', historiales=historiales, pacientes=pacientes)


@router2.route('/edit/historial/<int:id>', methods=['GET', 'POST'])
def edit_historial(id):
    historial = HistorialMedico.query.get(id)
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        try:
            historial.fecha = request.form['fecha']
            historial.diagnostico = request.form['diagnostico']
            historial.observaciones = request.form['observaciones']
            historial.idPaciente = request.form['idPaciente']

            db.session.commit()
            flash('Historial actualizado correctamente', 'success')
            return redirect(url_for('router2.list_historial'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el historial:', 'error')
            return redirect(url_for('router2.edit_historial', id=id))
    return render_template('/Historial/editar.html', historial=historial, pacientes=pacientes)



@router2.route('/delete/historial/<int:id>', methods=['GET'])
def delete_historial(id):
    try:
        historial = HistorialMedico.query.get_or_404(id)
        db.session.delete(historial)
        db.session.commit()
        flash('Historial eliminado correctamente', 'success')
        return redirect(url_for('router2.list_historial'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el historial:', 'error')
        return redirect(url_for('router2.register_historial'))
    























#rutas para tratamiento
@router2.route('/register/tratamiento', methods=['GET','POST'])
def register_tratamiento():
    historiales = HistorialMedico.query.all()
    pacientes = Paciente.query.all()

    if request.method == 'POST':
            try:
                nombre = request.form['nombre']
                descripcion = request.form['descripcion']
                duracion = request.form['duracion']
                medicamentos = request.form['medicamentos']
                idHistorial = request.form['idHistorial']
            
                if not nombre :
                        flash('Todos los campos son requeridos', 'error')
                        return redirect(url_for('router2.register_tratamiento'))
                tratamiento = Tratamiento(
                    nombre=nombre,
                    descripcion=descripcion,
                    duracion=duracion,
                    medicamentos=medicamentos,
                    idHistorial=idHistorial
                )
                db.session.add(tratamiento)
                db.session.commit()
                flash('Tratamiento registrado correctamente', 'success')
                return redirect(url_for('router2.list_tratamiento'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al guardar el tratamiento', 'error')
                return redirect(url_for('router2.register_tratamiento'))
            
    return render_template('/Tratamiento/registro.html', historiales=historiales, pacientes=pacientes,)




@router2.route('/list/tratamiento')
def list_tratamiento():
    tratamientos=Tratamiento.query.all()
    historiales=HistorialMedico.query.all()
    pacientes=Paciente.query.all()
    return render_template('/Tratamiento/lista.html',historiales=historiales, tratamientos=tratamientos, pacientes=pacientes)


@router2.route('/edit/tratamiento/<int:id>', methods=['GET', 'POST'])
def edit_tratamiento(id):
    tratamiento = Tratamiento.query.get(id)
    historiales = HistorialMedico.query.all()
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        try:
            tratamiento.nombre = request.form['nombre']
            tratamiento.descripcion = request.form['descripcion']
            tratamiento.duracion = request.form['duracion']
            tratamiento.medicamentos = request.form['medicamentos']
            tratamiento.idHistorial = request.form['idHistorial']

            db.session.commit()
            flash('Tratamiento actualizado correctamente', 'success')
            return redirect(url_for('router2.list_tratamiento'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el tratamiento:', 'error')
            return redirect(url_for('router2.edit_tratamiento', id=id))
    return render_template('/Tratamiento/editar.html', tratamiento=tratamiento, historiales=historiales, pacientes=pacientes)


@router2.route('/delete/tratamiento/<int:id>', methods=['GET'])
def delete_tratamiento(id):
    try:
        tratamiento = Tratamiento.query.get_or_404(id)
        db.session.delete(tratamiento)
        db.session.commit()
        flash('Tratamiento eliminado correctamente', 'success')
        return redirect(url_for('router2.list_tratamiento'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el tratamiento:', 'error')
        return redirect(url_for('router2.register_tratamiento'))





























#rutas para factura
@router2.route('/register/factura', methods=['GET','POST'])
def register_factura():
    citas = Citas.query.all()
    pacientes = Paciente.query.all()
    if request.method == 'POST':
            try:
                costo = request.form['costo']
                fecha = request.form['fecha']
                estado = request.form['estado']
                idCita = request.form['idCita']
            
                if not costo or not fecha or not estado:
                        flash('Todos los campos son requeridos', 'error')
                        return redirect(url_for('router2.register_factura'))
                factura = Factura(
                    costo=costo,
                    fecha=fecha,
                    estado=estado,
                    idCita=idCita
                )
                db.session.add(factura)
                db.session.commit()
                flash('Factura registrada correctamente', 'success')
                return redirect(url_for('router2.list_factura'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al guardar la factura', 'error')
                return redirect(url_for('router2.register_factura'))
            
    return render_template('/Factura/registro.html', citas=citas,pacientes=pacientes)


@router2.route('/list/factura')
def list_factura():
    facturas=Factura.query.all()
    citas=Citas.query.all()
    pacientes=Paciente.query.all()
    return render_template('/Factura/lista.html',facturas=facturas, citas=citas, pacientes=pacientes)




@router2.route('/edit/factura/<int:id>', methods=['GET', 'POST'])
def edit_factura(id):
    factura = Factura.query.get(id)
    citas = Citas.query.all()
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        try:
            factura.costo = request.form['costo']
            factura.fecha = request.form['fecha']
            factura.estado = request.form['estado']
            factura.idCita = request.form['idCita']

            db.session.commit()
            flash('Factura actualizada correctamente', 'success')
            return redirect(url_for('router2.list_factura'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la factura:', 'error')
            return redirect(url_for('router2.edit_factura', id=id))
    return render_template('/Factura/editar.html', factura=factura, citas=citas,pacientes=pacientes)



@router2.route('/delete/factura/<int:id>', methods=['GET'])
def delete_factura(id):
    try:
        factura = Factura.query.get_or_404(id)
        db.session.delete(factura)
        db.session.commit()
        flash('Factura eliminada correctamente', 'success')
        return redirect(url_for('router2.list_factura'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la factura:', 'error')
        return redirect(url_for('router2.register_factura'))