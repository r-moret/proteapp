import {
  AnimalSchema,
  TreatmentSchema,
  CreateAppointmentSchema,
  AppointmentSchema
} from './declarations'

export const AppointmentAdapter = (input: any) => AppointmentSchema.parse(input)
export const CreateAppointmentAdapter = (input: any) => CreateAppointmentSchema.parse(input)

export const TreatmentAdapter = (input: any) => TreatmentSchema.parse(input)
// TODO: Create TreatmentAdapter

export const AnimalAdapter = (input: any) => AnimalSchema.parse(input)
