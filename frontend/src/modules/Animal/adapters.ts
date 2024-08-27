import {
  AnimalSchema,
  AnimalInfoSchema,
  EditAppointmentSchema,
  EditTreatmentSchema,
  EditAnimalSchema,
  EnrichedEditAnimalSchema
} from './declarations'

export const EditAppointmentAdapter = (input: any) => EditAppointmentSchema.parse(input)
export const EditTreatmentAdapter = (input: any) => EditTreatmentSchema.parse(input)
export const EditAnimalAdapter = (input: any) => EditAnimalSchema.parse(input)
export const EnrichedEditAnimalAdapter = (input: any) => EnrichedEditAnimalSchema.parse(input)
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
