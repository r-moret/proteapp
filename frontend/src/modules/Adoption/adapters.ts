import {
  AdoptionInfoSchema,
  AdoptionSchema,
  EditMonitoringSchema,
  EditAdoptionSchema
} from './declarations'

export const AdoptionInfoAdapter = (input: any) => AdoptionInfoSchema.parse(input)
export const AdoptionAdapter = (input: any) => AdoptionSchema.parse(input)
export const EditMonitoringAdapter = (input: any) => EditMonitoringSchema.parse(input)
export const EditAdoptionAdapter = (input: any) => EditAdoptionSchema.parse(input)
