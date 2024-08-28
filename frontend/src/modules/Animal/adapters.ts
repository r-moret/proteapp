import {
  AnimalSchema,
  AnimalInfoSchema,
  EditAppointmentSchema,
  EditTreatmentSchema,
  EditAnimalSchema,
  EnrichedEditAnimalSchema
} from './declarations'
import { ImageAdapter } from '@/utils'

export const EditAppointmentAdapter = (input: any) => EditAppointmentSchema.parse(input)
export const EditTreatmentAdapter = (input: any) => EditTreatmentSchema.parse(input)
export const EditAnimalAdapter = (input: any) => EditAnimalSchema.parse(input)
export const EnrichedEditAnimalAdapter = (input: any) => EnrichedEditAnimalSchema.parse(input)
export const AnimalInfoAdapter = (input: any) => ImageAdapter(AnimalInfoSchema.parse(input))
export const AnimalAdapter = (input: any) => ImageAdapter(AnimalSchema.parse(input))
