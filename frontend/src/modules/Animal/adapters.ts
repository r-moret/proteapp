import {
  AnimalSchema,
  AnimalInfoSchema,
  EditAppointmentSchema,
  EditTreatmentSchema
} from './declarations'

export const EditAppointmentAdapter = (input: any) => EditAppointmentSchema.parse(input)
export const EditTreatmentAdapter = (input: any) => EditTreatmentSchema.parse(input)
export const AnimalInfoAdapter = (input: any) => {
  const animal = AnimalInfoSchema.parse(input)

  if (animal.image) {
    animal.image = `${import.meta.env.VITE_BACKEND_URL}/${animal.image}`
  }

  return animal
}
export const AnimalAdapter = (input: any) => {
  const animal = AnimalSchema.parse(input)

  if (animal.image) {
    animal.image = `${import.meta.env.VITE_BACKEND_URL}/${animal.image}`
  }

  return animal
}
