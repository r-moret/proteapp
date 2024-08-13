import {
  AnimalSchema,
  AnimalInfoSchema,
  EditAppointmentSchema,
  EditTreatmentSchema,
  EditYardSchema
} from './declarations'

export const EditAppointmentAdapter = (input: any) => EditAppointmentSchema.parse(input)
export const EditTreatmentAdapter = (input: any) => EditTreatmentSchema.parse(input)
export const AnimalInfoAdapter = (input: any) => AnimalInfoSchema.parse(input)
export const AnimalAdapter = (input: any) => AnimalSchema.parse(input)
export const EditYardAdapter = (input: any) => EditYardSchema.parse(input)
