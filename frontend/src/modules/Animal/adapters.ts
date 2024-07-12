import { AnimalSchema, TreatmentSchema } from './declarations'

export const TreatmentAdapter = (input: any) => TreatmentSchema.parse(input)

export const AnimalAdapter = (input: any) => AnimalSchema.parse(input)
